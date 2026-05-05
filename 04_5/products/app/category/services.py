from app.db.config import SessionDep
from app.category.schemas import CategoryCreate
from app.category.models import Category

async def create_category(new_category : CategoryCreate, session : SessionDep):
    category  = Category (
            name = new_category.name)
    session.add(category)
    session.commit()
    session.refresh(category )
    return category 