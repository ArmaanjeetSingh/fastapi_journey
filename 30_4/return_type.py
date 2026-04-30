from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id : int
    price : float
    name : str
    stock : int | None = None

class ProductOut(BaseModel):
    name : str
    price : float

app = FastAPI()


# Return type annotation
# @app.get("/products/")
# async def get_products()->Product:
#     return {"id":1,"price":305.67,"name":"Moto E"}

# @app.get("/products/")
# async def get_products()->List[Product]:
#     return [{"id":1,"price":305.67,"name":"Moto E"},
#          {"id":1,"price":305.67,"name":"Moto E"},]

@app.get("/products/",response_model = ProductOut)
async def get_products():
    return {"price":305.67,"name":"Moto E"}