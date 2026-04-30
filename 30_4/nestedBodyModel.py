from fastapi import FastAPI 
from pydantic import BaseModel, Field

app = FastAPI()


##Nested Body Model
class Category(BaseModel):
    name : str = Field(
        title = "Category Name",
        description = "The name of the product category",
        max_length = 50,
        min_length = 1
    ),
    description : str | None =  Field(
        default = None,
        title = 'category',
        description = 'A brief description of the category',
        max_length = 200
    )

class ProductModel(BaseModel):
    name : str
    stock : int
    price : float
    category : Category | None = None


app = FastAPI()

@app.post("/products")
async def create_product(product : ProductModel):
    return product