from fastapi import APIRouter, HTTPException, status, Depends
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session 
from ..models import Users
from passlib.context import CryptContext
from .auth import get_current_user
from pydantic import BaseModel


router = APIRouter(
    prefix = '/users',
    tags = ['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

class UserVerification(BaseModel):
    password : str
    new_password : str


@router.get("/",status_code = status.HTTP_200_OK)
async def get_user_info(db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authorized')
    return db.query(Users).filter(Users.id == user.get("id")).first()



@router.put("/",status_code = status.HTTP_204_NO_CONTENT)
async def change_user_password(user_verification_request : UserVerification, db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authorized')
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(user_verification_request.password, user_model.hashed_password):
        raise HTTPException(status_code = 401, detail = 'not authorized')
    user_model.hashed_password = bcrypt_context.hash(user_verification_request.new_password)
    db.add(user_model)
    db.commit()
