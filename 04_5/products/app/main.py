from fastapi import FastAPI
from app.product.schemas import ProductCreate
from app.category.schemas import CategoryCreate
from app.product.services import *
from app.category.services import *
from app.db.config import SessionDep

app = FastAPI()

@app.post("/category")
async def category_create(new_category  : CategoryCreate, session :SessionDep):
    category  = await create_category (new_category ,session)
    return category 

@app.post("/product")
async def product_create(new_product : ProductCreate, session :SessionDep):
    product = await create_product(new_product,session)
    return product