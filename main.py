from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home ():
    return{
        "message":"hello world"
    }
@app.post("/items")
def get_items(bike: str, car: str, cycle: str):
    return{
        "bike": bike,
        "car": car,
        "cycle": cycle
    }

@app.post("/items/{item_id}")
def get_item(item_id: int, name: str, price: float):
    return{
        "item_id": item_id,
        "name": name,
        "price": price
    }