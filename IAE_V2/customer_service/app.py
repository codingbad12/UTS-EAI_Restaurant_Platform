# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# In-memory storage
customers = []

# Models
class Customer(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    email: str
    phone: Optional[str] = None

# Customer Endpoints
@app.get("/customers", response_model=List[Customer])
def list_customers():
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers

@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    for customer in customers:
        if customer.id == customer_id:
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    if any(c.id == customer.id for c in customers):
        raise HTTPException(status_code=400, detail="Customer ID already exists")
    customers.append(customer)
    return customer

@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, updated_customer: Customer):
    for index, customer in enumerate(customers):
        if customer.id == customer_id:
            customers[index] = updated_customer
            return updated_customer
    raise HTTPException(status_code=404, detail="Customer not found")

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    for index, customer in enumerate(customers):
        if customer.id == customer_id:
            del customers[index]
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Customer not found")
