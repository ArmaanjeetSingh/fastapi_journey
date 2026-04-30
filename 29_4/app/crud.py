from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    title : Optional[str] = None
    price : Optional[float] = None
    description : Optional[str] = None

app = FastAPI()

PRODUCTS = [
    {
        "id":1,
        "title":"smart watch",
        "price":125.67,
        "description":"Perfect for young boys to wear, stylish brand"
    },
     {
        "id":2,
        "title":"men's jacket",
        "price":55.95,
        "description":"Great outfit jakcet for spring and autumn"
    },
     {
        "id":3,
        "title":"smart watch",
        "price":125.67,
        "description":"Perfect for young boys to wear, stylish brand"
    },
     {
        "id":4,
        "title":"sneakers shoes",
        "price":378.21,
        "description":"Perfect for young boys to wear, stylish brand"
    },
     {
        "id":5,
        "title":"smart watch",
        "price":125.67,
        "description":"Perfect for young boys to wear, stylish brand"
    }
]


#GET
## Read or fetch all data
@app.get("/products",status_code = status.HTTP_200_OK)
async def all_products():
    return PRODUCTS


#GET
## Read or fetch single data
@app.get("/products/{product_id}",status_code = status.HTTP_200_OK)
async def all_products(product_id : int):
    for product in PRODUCTS:
        if product.get("id") == product_id:
            return product
    return {"response":"no product found"}



## POST
## Create or Insert data
@app.post("/product",status_code = status.HTTP_201_CREATED)
async def create_product(new_product:Product):
    new_product = new_product.model_dump()
    new_product['id'] = len(PRODUCTS)+1
    PRODUCTS.append(new_product)
    return {"status":"created","new_product":new_product}



## PUT
## Update data
@app.put("/product/{product_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_product(new_product : Product,product_id : int):
    for index,product in enumerate(PRODUCTS):
        if product_id == product.get("id"):
            product.update(**new_product.model_dump())
            return {"status":"product updated","updated_product":product}
    return {"status":"no product found"}


## PATCH
## Partial Update data
@app.patch("/product/{product_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_product(new_product : Product,product_id : int):
    for index,product in enumerate(PRODUCTS):
        if product_id == product.get("id"):
            product.update(new_product.dict(exclude_unset = True))
            return {"status":"product updated","patial_updated_product":product}
    return {"status":"no product found"}


## DELETE 
## delete data
@app.delete("/product/{product_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_product(product_id : int):
    for product in PRODUCTS:
        if product.get("id") == product_id:
            PRODUCTS.remove(product)
            return {"status":"product removed","delted":product}
    return {"status":"not found"}