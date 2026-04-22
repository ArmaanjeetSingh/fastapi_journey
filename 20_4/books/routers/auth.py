from fastapi import APIRouter,Depends, status, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError

from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from datetime import datetime
from datetime import timedelta, timezone

class CreateUserRequest(BaseModel):
   username : str
   email : str
   first_name : str
   last_name : str
   password : str
   role : str


class Token(BaseModel):
   access_token : str
   token_type : str


router = APIRouter(
   prefix = '/auth',
   tags = ['auth']
)
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')

SECRET_KEY = '452ac292de00959fbc583a56d8bb4fa691aa089cd336c64141ba968b138d7fc2'
ALGORITHM = 'HS256'

def get_db():
   db = SessionLocal()
   try:
      yield db 
   finally:
      db.close()
db_dependency = Annotated[Session,Depends(get_db)]


def authenticate_user(username : str, password : str, db):
   user = db.query(Users).filter(Users.username == username).first()
   if not user:
      return False
   if not bcrypt_context.verify(password, user.hashed_password):
      return False
   return user


def create_access_token(username : str, user_id : int, role : str, expires_delta : timedelta):
   encode = {'sub':username, 'id': user_id, 'role' : role}
   expires = datetime.now(timezone.utc) + expires_delta
   encode.update({'exp':expires})
   return jwt.encode(encode,SECRET_KEY,algorithm = ALGORITHM)


async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
   try :
      payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
      username : str = payload.get('sub')
      user_id : int = payload.get('id')
      user_role : str = payload.get('role')

      if username is None or user_id is None:
         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'could not found user')
      return {'username':username, 'id':user_id, 'user_role':user_role}
   except JWTError:
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'could not found user')

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/auth/")
async def create_user(create_user_request : CreateUserRequest, db :db_dependency, status_code = status.HTTP_201_CREATED):
   create_user_model  = Users(
      email = create_user_request.email,
      username = create_user_request.username,
      first_name = create_user_request.first_name,
      last_name = create_user_request.last_name,
      hashed_password = bcrypt_context.hash(create_user_request.password),
      role = create_user_request.role,
      is_active = True
   )
   db.add(create_user_model)
   db.commit()


@router.post("/token",response_model = Token)
def login_for_access_token_(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
                          db : db_dependency):
      user = authenticate_user(form_data.username,form_data.password,db)
      if not user:
         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'could not found user')
      token = create_access_token(user.username,user.id,user.role,timedelta(minutes = 30))
      return {'access_token':token,'token_type':'bearer'}


# get_user: this endpoint should return all information about the user that is currently logged in
@router.get("/get_user")
def get_user(db : db_dependency, user: user_dependency):
   if not user:
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'could not found user')
   user_info = db.query(Users).filter(Users.id == user.get('id')).first()
   return user_info


# change_password: this endpoint should allow a user to change their current password
@router.put("/change_password")
async def change_password(old_password : str,new_password : str,db : db_dependency, user : user_dependency):
   if not user:
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'could not found user')
   user_info_model = db.query(Users).filter(Users.id == user.get('id')).first()
   if not bcrypt_context.verify(old_password,user_info_model.hashed_password):
      raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = 'incorrect password')
   user_info_model.hashed_password = bcrypt_context.hash(new_password)
   db.add(user_info_model)
   db.commit()