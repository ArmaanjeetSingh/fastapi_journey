from app.db.config import SessionDep
from app.product.schemas import ProductCreate
from app.product.models import Product

async def create_product(new_product : ProductCreate, session : SessionDep):
    product = Product(
            name = new_product.name, 
            price = new_product.price, 
            stock = new_product.stock,
            category_id = new_product.category_id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product