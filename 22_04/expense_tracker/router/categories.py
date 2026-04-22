from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session 
from database import SessionLocal,engine
from models import Category, Transactions
from typing import Annotated, Literal, Optional
from .users import get_current_user

from pydantic import BaseModel, Field

user_dependency = Annotated[dict,Depends(get_current_user)]

class CategoryRequest(BaseModel):
    name : str = Field(min_length = 3, max_length = 20)
    type : Literal['Housing','Food','Transport','Health and wellness']


router = APIRouter(
    prefix = "/categories",
    tags = ['category']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


@router.post("/",status_code = status.HTTP_201_CREATED)
async def create_category(category : CategoryRequest,user : user_dependency, db : db_dependency):
    category_model = Category(
        name = category.name,
        type = category.type,
        user_id = user.get("id") 
    )
    print(category_model)
    db.add(category_model)
    db.commit()


@router.get("/",status_code = status.HTTP_200_OK)
async def get_category(user : user_dependency, db : db_dependency):
    response = db.query(Category).filter(Category.user_id == user.get("id")).all()
    if response is None:
        return HTTPException(status_code = 400, detail = f'no content found')
    return response

@router.get("/{id}",status_code = status.HTTP_200_OK)
async def get_category_by_id(id : int,user : user_dependency, db : db_dependency):
    response = db.query(Category).filter(Category.user_id == user.get("id")).filter(Category.id == id).first()
    if response is None:
        return HTTPException(status_code = 400, detail = f'no content found')
    return response


@router.put("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def get_category(category : CategoryRequest,user : user_dependency, db : db_dependency, id : int = Path(gt = 0)):
    response = db.query(Category).filter(Category.user_id == user.get("id")).filter(Category.id == id).first()
    if response is None:
        return HTTPException(status_code = 400, detail = f'no content found')
    response.name = category.name
    response.type = category.type
    db.add(response)
    db.commit()


@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def get_category(category : CategoryRequest,user : user_dependency, db : db_dependency, id : int = Path(gt = 0)):
    response = db.query(Category).filter(Category.user_id == user.get("id")).filter(Category.id == id).first()
    if response is None:
        return HTTPException(status_code = 400, detail = f'no content found')
    db.delete(response)
    db.commit()