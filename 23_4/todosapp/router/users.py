from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users, Todos
from fastapi import status, HTTPException
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

@router.get("/",status_code = status.HTTP_200_OK)
async def get_user(db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication Failed')
    return db.query(Users).filter(Users.id == user.get("id")).first()


class UserVerification(BaseModel):
    password : str
    new_password : str

@router.get("/",status_code = status.HTTP_200_OK)
async def get_user(db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication Failed')
    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password",status_code = status.HTTP_204_NO_CONTENT)
async def change_password(user :user_dependency, db : db_dependency, user_verification : UserVerification):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication Failed')
    print(user)
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    print(user_model)
    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code = 401, detail = 'Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.password)
    db.add(user_model)
    db.commit()
