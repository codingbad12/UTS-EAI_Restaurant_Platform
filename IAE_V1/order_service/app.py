# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import requests

app = FastAPI()

# In-memory storage
orders = []

# Models
class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)

class Order(BaseModel):
    id: int
    customer_id: int
    items: List[OrderItem]
    total_price: Optional[float] = 0.0

# Service base URLs (mocked locally)
MENU_SERVICE_URL = "http://localhost:8000/menu-items/"
CUSTOMER_SERVICE_URL = "http://localhost:8001/customers/"

# Helpers
def fetch_menu_item(menu_item_id: int):
    response = requests.get(f"{MENU_SERVICE_URL}{menu_item_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Invalid menu item ID: {menu_item_id}")
    return response.json()

def verify_customer(customer_id: int):
    response = requests.get(f"{CUSTOMER_SERVICE_URL}{customer_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid customer ID")

# Endpoints
@app.get("/orders", response_model=List[Order])
def list_orders():
    return orders

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    for order in orders:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders", response_model=Order)
def create_order(order: Order):
    if any(o.id == order.id for o in orders):
        raise HTTPException(status_code=400, detail="Order ID already exists")

    verify_customer(order.customer_id)

    total_price = 0.0
    for item in order.items:
        menu_data = fetch_menu_item(item.menu_item_id)
        if not menu_data["available"]:
            raise HTTPException(status_code=400, detail=f"Menu item '{menu_data['name']}' is not available")
        total_price += menu_data["price"] * item.quantity

    order.total_price = total_price
    orders.append(order)
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for index, order in enumerate(orders):
        if order.id == order_id:
            del orders[index]
            return {"message": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")
