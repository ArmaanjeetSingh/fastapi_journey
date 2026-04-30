from fastapi import APIRouter, status, HTTPException, Depends
from .auth import get_current_user
from ..database import SessionLocal
from ..models import Expenses, Category
from typing import Annotated
from sqlalchemy.orm import Session 
from pydantic import BaseModel, computed_field
from datetime import datetime
from datetime import datetime, timezone

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CategoryRequest(BaseModel):
    name : str
    description : str

router = APIRouter(
    prefix = '/categories',
    tags = ['categories']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/",status_code = status.HTTP_201_CREATED)
async def create_category(create_category_request : CategoryRequest, db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')
    create_category_model = Category(
        name = create_category_request.name,
        description = create_category_request.description
    )
    db.add(create_category_model)
    db.commit()


@router.get("/",status_code = status.HTTP_200_OK)
async def get_category(db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')

    return db.query(Category).all()

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def get_category(id : int,db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')

    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code = 404,detail = 'not found category')
    db.delete(category)
    db.commit()
