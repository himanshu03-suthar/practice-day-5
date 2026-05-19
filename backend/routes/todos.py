import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo
from schemas import TodoCreate, TodoOut, TodoUpdate

router = APIRouter(prefix="/todos", tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_due_date(date_text: Optional[str]) -> Optional[datetime]:
    if not date_text:
        return None

    for formatted in (date_text, f"{date_text}T00:00:00"):
        try:
            return datetime.fromisoformat(formatted)
        except ValueError:
            continue

    return None


def build_notification_item(task: Todo) -> dict:
    return {
        "id": task.id,
        "title": task.title,
        "due_date": task.due_date,
        "priority": task.priority,
        "status": task.status,
        "is_monitored": task.is_monitored,
    }


def get_upcoming_notifications(db: Session, within_hours: int = 24) -> List[Todo]:
    now = datetime.utcnow()
    threshold = now + timedelta(hours=within_hours)
    result = []

    for task in db.query(Todo).all():
        due = parse_due_date(task.due_date)
        if due is None:
            continue

        if due <= now:
            result.append(task)
            continue

        if now < due <= threshold:
            result.append(task)

    return result


@router.get("/", response_model=List[TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return db.query(Todo).order_by(Todo.priority.desc(), Todo.due_date).all()


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return todo


@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    todo = Todo(
        title=payload.title,
        description=payload.description or "",
        due_date=payload.due_date or "",
        priority=payload.priority or 3,
        status=payload.status or "pending",
        is_monitored=payload.is_monitored or False,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(todo)
    db.commit()


@router.post("/{todo_id}/toggle-monitor", response_model=TodoOut)
def toggle_monitor(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    todo.is_monitored = not todo.is_monitored
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/monitor", response_model=List[TodoOut])
def get_monitored_tasks(db: Session = Depends(get_db)):
    return db.query(Todo).filter(Todo.is_monitored.is_(True)).order_by(Todo.priority.desc(), Todo.due_date).all()


@router.get("/notifications")
def get_notifications(db: Session = Depends(get_db)):
    tasks = get_upcoming_notifications(db)
    return {
        "count": len(tasks),
        "notifications": [
            {
                "task": task.title,
                "due_date": task.due_date,
                "priority": task.priority,
                "status": task.status,
                "reason": "overdue" if parse_due_date(task.due_date) <= datetime.utcnow() else "due soon",
            }
            for task in tasks
        ],
    }


@router.websocket("/notifications/ws")
async def notifications_ws(websocket: WebSocket):
    await websocket.accept()
    db = SessionLocal()
    try:
        while True:
            tasks = get_upcoming_notifications(db, within_hours=24)
            payload = {
                "count": len(tasks),
                "notifications": [
                    {
                        "task": task.title,
                        "due_date": task.due_date,
                        "priority": task.priority,
                        "status": task.status,
                    }
                    for task in tasks
                ],
            }
            await websocket.send_json(payload)
            await asyncio.sleep(15)
    except WebSocketDisconnect:
        return
    finally:
        db.close()
