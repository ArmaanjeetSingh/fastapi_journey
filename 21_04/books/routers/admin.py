from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session
from models import Books

from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(
    prefix = '/admin',
   tags = ['admin']
)

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
    print(user['user_role'])
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    return db.query(Books).all()


@router.delete("/book/{book_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(user : user_dependency, db : db_dependency,book_id : int = Path(gt = 0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    book_model = db.query(Books).filter(Books.id == book_id)
    if book_model is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    db.delete(book_model)
    db.commit()


