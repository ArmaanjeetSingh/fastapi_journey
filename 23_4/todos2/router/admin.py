from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos

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


@router.get("/todo")
async def read_all(db :db_dependency,user : user_dependency):
    if user.get('role') != 'admin':
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency, db : db_dependency,todo_id : int = Path(gt = 0)):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'no user validate')
    todo_model = db.query(Todos).filter(Todos.id == todo_id)
    if todo_model is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    db.delete(todo_model)
    db.commit()


