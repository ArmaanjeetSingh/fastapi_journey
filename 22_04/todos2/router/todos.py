from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import session
from pydantic import BaseModel, Field
from router import auth
from .auth import get_current_user

router = APIRouter()

router.include_router(auth.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title : str = Field(min_length=2)
    description : str = Field(min_length=3, max_lenght= 50)
    priority : int = Field(gt = 0, lt = 6)
    complete : bool


@router.get("/")
async def read_all(user : user_dependency,db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get('id'))


@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = 'Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).\
        filter(Todos.owner_id == users.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail=f'Todo not found')


@router.post("/todo",status_code = status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db : db_dependency, todo_request : TodoRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = 'Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(),owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db : db_dependency,
                      todo_request : TodoRequest,
                      todo_id : int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail = f'Todo not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description    
    todo_model.priorty = todo_request.priority    
    todo_model.complete = todo_request.complete  

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db : db_dependency,
                      todo_id : int = Path(gt = 0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id)
    if todo_model is None:
        raise HTTPException(status_code=404,detail=f'tod id not found')
        
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()