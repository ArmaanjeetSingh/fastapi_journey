from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users, Todos
from fastapi import status, HTTPException
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

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.get("/todo",status_code = status.HTTP_200_OK)
async def read_all(user : user_dependency, db : db_dependency):
    # print(user)
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code = 401, detail = 'Authentication Failed')
    return db.query(Todos).all()



@router.delete("/todo/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency, db : db_dependency,id : int):
    if user is None or user.get("role") != 'admin':
        raise HTTPException(status_code = 401, detail = 'authentication failed')
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = 'no todo found')
    db.delete(todo_model)
    db.commit()