from fastapi import FastAPI
from app.db.config import create_tables
from app.user.services import *
from app.user.models import UserCreate,UserOut
from app.product.models import ProductCreate, ProductOut, ProductUpdate
from app.product.services import *
from contextlib import asynccontextmanager
from app.db.config import SessionDep

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan = lifespan)


@app.post("/user",response_model = UserOut)
async def user_create(user_input : UserCreate, session : SessionDep):
    print(user_input)
    user = await create_user(user_input,session)
    return user

@app.delete("/user/{id}")
async def user_delete(id : int, session : SessionDep):
    await delete_user(id,session)
    return {"message":"user deleted"}

@app.post("/product",response_model = ProductOut)
async def product_create(product_ip : ProductCreate, session : SessionDep):
    product = await create_product(product_ip,session)
    return product


@app.get("/product",response_model = list[ProductOut])
async def product_get_all(session : SessionDep):
    product = await get_all_products(session)
    return product


@app.get("/product/{product_id}",response_model = ProductOut)
async def product_get_all(product_id : int, session : SessionDep):
    product = await get_product_by_id(product_id,session)
    return product


@app.put("/product/{product_id}",response_model = ProductOut)
async def product_update(product_id : int,new_product:ProductUpdate, session : SessionDep):
    product = await update_product(product_id,new_product,session)
    return product


@app.delete("/product/{product_id}")
async def product_delete(product_id : int, session : SessionDep):
    product = await delete_product(product_id,session)
    return product