from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from database import SessionLocal,engine
from models import Users
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime
from datetime import timedelta, timezone
from jose import jwt, JWTError

class CreateUserRequest(BaseModel):
    name : str = Field(max_length = 20)
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

router = APIRouter(
    prefix = "/auth",
    tags = ['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
SECRET_KEY = "5e336e9ecd142baade4911f29b29ffb0c4cbc2ee48238e7a44953d0fa99ead63"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = '/auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

def get_authenticate_user(username : str, password : str, db):
    user_model = db.query(Users).filter(Users.name == username).first()
    if not user_model:
        raise HTTPException(status_code = 404, detail = f'no such user found')
    if not bcrypt_context.verify(password, user_model.hashed_password):
        raise HTTPException(status_code = 400, detail = f'incorrect password')
    print(user_model.name)
    return user_model


def create_access_token(username : str, id : int, expiry_timedelta : timedelta):
    encode = {'sub':username,'id':id}
    expires = datetime.now(timezone.utc) + expiry_timedelta
    encode.update({'expires':str(expires)})
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)


async def get_current_user(token : Annotated[dict,Depends(oauth2_bearer)]):
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : int = payload.get("id")
        name : str = payload.get("sub")
        if id is None or name is None:
            raise HTTPException(status_code = 404,detail = f'could not found user')
        return {'username':name,'id':id}
    except JWTError:
        raise HTTPException(status_code = 404,detail = f'could not found user')

user_dependency = Annotated[dict,Depends(get_current_user)]

@router.post("/register",status_code = status.HTTP_201_CREATED)
def create_user(create_user_request : CreateUserRequest, db : db_dependency):
    new_user = Users(
        email = create_user_request.email,
        name = create_user_request.name,
        hashed_password = bcrypt_context.hash(create_user_request.password)
    )
    db.add(new_user)
    db.commit()


@router.post("/token",status_code = status.HTTP_201_CREATED,response_model = Token)
def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db : db_dependency):
    user = get_authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = 'Invalid credentials')
    print(user.id)
    token = create_access_token(user.name, user.id, timedelta(minutes = 20))
    return {'access_token':token,'token_type':'bearer'}


@router.get("/me",status_code = status.HTTP_200_OK)
def get_current_user_logged_in(user : user_dependency):
    return user