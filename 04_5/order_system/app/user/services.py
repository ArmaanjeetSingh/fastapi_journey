from app.user.models import UserCreate, User
from app.db.config import SessionDep
from sqlmodel import select, Session
from fastapi import HTTPException


async def create_user(user : UserCreate, session : SessionDep):
    create_user_model = User(**user.model_dump())
    session.add(create_user_model)
    session.commit()
    session.refresh(create_user_model)
    return create_user_model


async def delete_user(user_id : int, session : SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code = 404, detail = 'user not found')

    session.delete(user)
    session.commit()