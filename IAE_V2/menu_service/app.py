# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# In-memory storage
menu_items = []
categories = []

# Models
class Category(BaseModel):
    id: int
    name: str

class MenuItem(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str
    available: bool = True

# Category Endpoints
@app.get("/menu-items", response_model=List[MenuItem])
def list_menu_items():
    if not menu_items:
        raise HTTPException(status_code=404, detail="No menu items found")
    return menu_items

@app.post("/categories", response_model=Category)
def create_category(category: Category):
    if any(c.id == category.id for c in categories):
        raise HTTPException(status_code=400, detail="Category ID already exists")
    categories.append(category)
    return category

# Menu Item Endpoints
@app.get("/categories", response_model=List[Category])
def list_categories():
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories

@app.get("/menu-items/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: int):
    for item in menu_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Menu item not found")

@app.post("/menu-items", response_model=MenuItem)
def create_menu_item(item: MenuItem):
    if any(i.id == item.id for i in menu_items):
        raise HTTPException(status_code=400, detail="Menu item ID already exists")
    menu_items.append(item)
    return item

@app.put("/menu-items/{item_id}", response_model=MenuItem)
def update_menu_item(item_id: int, updated_item: MenuItem):
    for index, item in enumerate(menu_items):
        if item.id == item_id:
            menu_items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Menu item not found")

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id: int):
    for index, item in enumerate(menu_items):
        if item.id == item_id:
            del menu_items[index]
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Menu item not found")
