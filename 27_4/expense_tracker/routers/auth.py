from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session 
from ..models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime
from datetime import timedelta, timezone
from jose import jwt, JWTError
from fastapi import Request
from fastapi.templating import Jinja2Templates


class CreateUserRequest(BaseModel):
    name : str 
    email : EmailStr 
    password : str
    role : str

class Token(BaseModel):
    access_token : str
    token_type : str

router = APIRouter(
    prefix = '/auth',
    tags  = ['auth']
)
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
SECRET_KEY = "f62563ac776bf1a3463c3cca0ba497fb4c050dd8b5f817d7b41ee5c2e2e4760b"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = '/auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory=r"D:\denama\fastapi\27_4\expense_tracker\templates")

## PAGES

@router.get("/login-page")
def render_login_page(request : Request):
    return templates.TemplateResponse(name = "login.html", request = request, context = {})

@router.get("/register-page")
def render_login_page(request : Request):
    return templates.TemplateResponse(name = "register.html", request = request, context = {})


## ENDPOINTS
async def get_authenticate_user(username : str, password : str, db : db_dependency):
    user_model = db.query(Users).filter(Users.name == username).first()
    print(user_model.hashed_password)
    if not user_model:
        # raise HTTPException(status_code = 404, detail = 'user not found')
        return None
    if not bcrypt_context.verify(password, user_model.hashed_password):
        return None
    return user_model


def create_access_token(username : str, role : str, id : int, expires_delta : timedelta):
    encode = {'sub':username,'role':role,'id':id}
    expires = str(datetime.now(timezone.utc)+ expires_delta)
    encode.update({'expires':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)


async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        username : str = payload.get("sub")
        id : int = payload.get("id")
        role : str = payload.get("role")
        if username is None or id is None:
            raise HTTPException(status_code=401, detail = 'not authorized user')
        return {'username':username,'id':id,"role":role}
    except JWTError :
        raise HTTPException(status_code=401, detail = 'not authorized user')
    

@router.post("/",status_code= status.HTTP_201_CREATED)
async def create_user(db : db_dependency,create_user_request : CreateUserRequest):
    create_user_model  = Users(
        name = create_user_request.name,
        email = create_user_request.email,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role =  create_user_request.role  
    )
    # print(create_user_model)
    db.add(create_user_model)
    db.commit()


@router.post("/token",response_model = Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()] ,db : db_dependency):
    user = await get_authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code = 401, detail = 'invalid password')
    token = create_access_token(user.name, user.role, user.id, timedelta(minutes = 20))
    return {'access_token': token, 'token_type':'bearer'}


