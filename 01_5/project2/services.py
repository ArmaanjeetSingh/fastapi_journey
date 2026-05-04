from models import User
from db import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends


async def get_db():
    async with async_session() as db:
        yield db


db_dependency = Annotated[AsyncSession,Depends(get_db)]

async def create_user(name : str, email : str, db : db_dependency):
    user_model = User(name = name, email = email)
    db.add(user_model)
    await db.commit()