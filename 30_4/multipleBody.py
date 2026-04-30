from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Annotated

app = FastAPI()

## Multiple Body Parameters
class Product(BaseModel):
    name : str
    price : float
    stock : int | None = None


class Seller(BaseModel):
    username : str
    full_name : str | None = None


# @app.post("/product")
# async def create_product(seller : Seller,product : Product | None =  None):
#     return {"product":product, "seller":seller}

# @app.post("/optional/product")
# async def create_product(product : Product, seller : Optional[Seller] = None):
#     return {"product":product, "seller":seller}


## Singular values in body
@app.post("/product")
async def create_product(product : Product,secret_key : Annotated[str, Body()], seller : Optional[Seller] = None):
    return {"product":product, "seller":seller}