from fastapi import FastAPI
from pydantic import BaseModel, computed_field

app = FastAPI()

## With Pydantic
## Define the Product Model
class Product(BaseModel):
    id : int
    name : str
    price : float
    stock : int | None = None # Optional

    @computed_field
    def price_with_tax(self)->float:
        return self.price + self.price * 0.18


# @app.post("/product")
# async def create_product(new_product : Product):
#     return new_product

## Access attribute inside function
# @app.post("/product")
# async def create_product(new_product : Product):
#     print(new_product.id)
#     print(new_product.name)
#     print(new_product.price)
#     print(new_product.stock)


## Add new calculated attribute

@app.post("/product")
async def create_product(new_product : Product):
    product_dict = new_product.model_dump()
    # price_with_tax = new_product.price + (new_product.price * 0.18)
    # product_dict.update({"price_with_tax":price_with_tax})
    return product_dict


## Combinig request body with path params
@app.put("/products/{product_id}")
async def update_product(product_id : int, new_updated_product : Product):
    return {"product_id":product_id,'new_updated_product':new_updated_product}