from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users, Todos
from fastapi import status, HTTPException
from .auth import get_current_user

class TodoRequest(BaseModel):
    title : str
    description : str
    priority : int
    complete : bool

router = APIRouter(
    prefix = '/todos',
    tags = ['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


@router.post("/todo",status_code = status.HTTP_201_CREATED)
async def create_todo(user : user_dependency, db : db_dependency, todo_request : TodoRequest):
    if user is None:
        raise HTTPException(status_code = 404, detail = 'authentication failed')
    todo_model = Todos(**todo_request.model_dump(),owner_id = user.get("id"))
    db.add(todo_model)
    db.commit()


@router.get("/todo",status_code = status.HTTP_200_OK)
async def get_todo(user : user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'authentication failed')
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = 'no todo found')
    return todo_model



@router.get("/todo/{id}",status_code = status.HTTP_200_OK)
async def get_todo_by_id(user : user_dependency, db : db_dependency, id : int):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'authentication failed')
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).filter(Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = 'no todo found')
    return todo_model


@router.put("/todo/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_todo(user : user_dependency, db : db_dependency, todo_request : TodoRequest, id : int):
    if user is None:
        raise HTTPException(status_code = 404, detail = 'authentication failed')
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).filter(Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = 'no todo found')
    print(todo_model)
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.complete = todo_request.complete
    todo_model.priority = todo_request.priority
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency, db : db_dependency,id : int):
    if user is None:
        raise HTTPException(status_code = 404, detail = 'authentication failed')
    todo_model = db.query(Todos).filter(Todos.owner_id == user.get("id")).filter(Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code = 404, detail = 'no todo found')
    db.delete(todo_model)
    db.commit()