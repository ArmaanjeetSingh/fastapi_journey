from app.product.models import ProductCreate, Product, ProductUpdate
from sqlmodel import select, Session
from app.db.config import SessionDep
from fastapi import HTTPException


async def create_product(product : ProductCreate, session : SessionDep):
    print(product)
    create_product_model = Product(**product.model_dump())
    session.add(create_product_model)
    session.commit()
    session.refresh(create_product_model)
    return create_product_model


async def get_all_products(session : SessionDep):
    stmt = select(Product)
    result = session.exec(stmt)
    return result.all()


async def get_product_by_id(product_id : int,session : SessionDep):
    result = session.get(Product, product_id)
    if result is None:
        raise HTTPException(status = 404, detail = f'Product not found')
    return result


async def update_product(product_id : int,new_product : ProductUpdate, session : SessionDep):
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status = 404, detail = f'Product not found')
    product.quantity = new_product.quantity
    product.price  = new_product.price
    product.user_id = new_product.user_id
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
    
async def delete_product(product_id : int,session : SessionDep):
    result = session.get(Product, product_id)
    if result is None:
        raise HTTPException(status = 404, detail = f'Product not found')
    session.delete(result)
    session.commit()
    return {"message":"product deleted"}