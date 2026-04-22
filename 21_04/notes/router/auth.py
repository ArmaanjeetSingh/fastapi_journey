from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#pip install python-multipart
from datetime import datetime
from datetime import timedelta,timezone
from database import SessionLocal
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from jose import jwt
# pip install "python-jose[cryptography]"

class CreateUserRequest(BaseModel):
    username : str
    first_name : str
    last_name : str
    email : str
    password : str
    is_active : bool
    role : str

class Token(BaseModel):
    access_token : str
    token_type : str


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


def get_db():
    db = SessionLocal()
    try :
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
SECRET_KEY = "5c417e8a400a2e3aaad2fdc4d1bb2d61e21fa7c1cd2bf5c1d5d49ff0b60a2d5a"
ALGORITHM = "HS256"
oauth2bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

def authenticate_user(username : str, password : str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user :
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user


def create_access_token(username : str, id : int, role : str, expiry_timedelta : timedelta):
    encode = {'sub':username,'role':role,'id':id}
    expires = datetime.now(timezone.utc) + expiry_timedelta
    encode.update({'expires':str(expires)})
    return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)


async def get_current_user(token : Annotated[str, Depends(oauth2bearer)]):
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORIHTMS])
        username = payload.get("username")
        role = payload.get("role")
        id = payload.get("id")
        if username is None or user_id is None:
           raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'could not found user')
        return {"username":username,"role":role,"id":id}
    except JWTError:
        raise HTTPException(status_code=404,detail = 'could not found such user')

user_dependency = Annotated[dict,Depends(get_current_user)]

@router.post("/create_user",status_code = status.HTTP_201_CREATED)
def create_user(create_user_request : CreateUserRequest, db : db_dependency):
    create_user_model = Users(
        role = create_user_request.role,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        username = create_user_request.username,
        email = create_user_request.email,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = 1
    )
    print(create_user_model)
    db.add(create_user_model)
    db.commit()


@router.post("/token",status_code = status.HTTP_201_CREATED,response_model =Token)
async def login_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()], db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes = 20))
    return {'access_token':token,'token_type':'bearer'}