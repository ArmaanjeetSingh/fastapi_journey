from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session
from models import Books

from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user

class BookRequest(BaseModel):
    title : str = Field(max_length = 50)
    description : str | None = Field(max_length = 50)
    rating : int = Field(gt = 0)
    is_available : bool

class Book(BaseModel):
    id : int = Field(gt = 0)
    title : str = Field(max_length = 50)
    description : str | None = Field(max_length = 50)
    rating : int = Field(gt = 0)
    is_available : bool


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def read_all(db :db_dependency,user : user_dependency):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    return db.query(Books).filter(Books.owner_id == user.get('role')).all()


@router.get("/book/{book_id}",status_code = status.HTTP_200_OK)
async def read_book(user: user_dependency,db : db_dependency,book_id : int = Path(gt = 0)):
    book_model = db.query(Books).filter(Books.id == book_id).first()
    if book_model is not None:
        return book_model
        
    raise HTTPException(status_code = 404, detail = f'book not found')


@router.post("/book",status_code = status.HTTP_201_CREATED)
async def add_book(user: user_dependency, db : db_dependency, book : BookRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    new_book_model = Books (
        title = book.title,
        description = book.description,
        rating = book.rating,
        is_available = book.is_available,
        owner_id = user.get('id')
    )
    db.add(new_book_model)
    db.commit()


@router.put("/book/{book_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_book(user : user_dependency, db : db_dependency, book_request: Book):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    book_model = db.query(Books).filter(Books.id == book_request.id).filter(Books.owner_id == user.get("id")).first()
    print(book_model.title)
    if book_model is None:
        raise HTTPException(status_code = 404, detail = f'no such book found')
    book_model.title = book_request.title
    book_model.description = book_request.description
    book_model.rating = book_request.rating
    book_model.is_available = book_request.is_available

    print(book_model)

    db.add(book_model)
    db.commit()


@router.delete("/book/{book_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db : db_dependency, book_id : int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    book_model = db.query(Books).filter(Books.id == book_id).filter(Books.owner_id == user.get("id")).first()
    if book_model is None:
        raise HTTPException(staus_code = 404, detail = f'no book found')
    db.delete(book_model)
    db.commit()