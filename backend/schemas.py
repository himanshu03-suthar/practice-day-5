from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., example="Buy groceries")
    description: Optional[str] = Field("", example="Milk, eggs, and bread")
    due_date: Optional[str] = Field(None, example="2026-05-20T18:00:00")
    priority: Optional[int] = Field(3, ge=1, le=5, example=3)
    status: Optional[str] = Field("pending", example="pending")
    is_monitored: Optional[bool] = Field(False, example=True)


class TodoCreate(TodoBase):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    is_monitored: Optional[bool] = None


class TodoOut(TodoBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
