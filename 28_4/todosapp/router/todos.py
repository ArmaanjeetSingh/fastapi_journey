from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users, Todos
from fastapi import status, HTTPException
from .auth import *
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory = 'templates')

class TodoRequest(BaseModel):
    title : str
    description : str
    priority : int
    complete : bool

def redirect_to_login():
    redirect_response = RedirectResponse(url = '/auth/login-page',status_code = 302)
    redirect_response.delete_cookie(key = 'access_token')
    return redirect_response


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

## PAGES
@router.get("/todo-page")
async def render_todo_page(request : Request, db : db_dependency):
    token = request.cookies.get('access_token')
    if token is None:
        return redirect_to_login() 
    user = await get_current_user(token)
    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    print(todos)
    return templates.TemplateResponse(
        name="todos.html",request = request, 
        context={"request": request, "todos": todos,"user":user}
    )


# Create this helper function that doesn't use 'Depends'
def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            return None
        return {'username': username, 'id': user_id, "role": role}
    except JWTError:
        return None


@router.get("/add-todo-page")
async def render_todo_page(request: Request):
    token = request.cookies.get('access_token')
    
    if token is None:
        return redirect_to_login()

    # Use the clean helper function, NOT the one with Depends
    user = get_user_from_token(token)
    
    if user is None:
        return redirect_to_login()
    
    return templates.TemplateResponse(
    request=request, 
    name="add_todo.html", 
    context={"user": user}
    )


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request : Request,todo_id : int):
    try :
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse("edit_todo.html",request = request,context = {"request" : request, "todo":todo})
    except:
        return redirect_to_login()


## ENDPOINTS

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