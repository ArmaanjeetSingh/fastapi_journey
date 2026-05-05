from db import engine
from models import User
from sqlmodel import Session, select


def create_user(name : str, email : str):
    with Session(engine) as session:
        user = User(name = name,email = email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_all_users():
    with Session(engine) as session:
        stmt = select(User)
        users = session.scalars(stmt)
        return users.all()


def get_user_by_id(id : int):
    with Session(engine) as session:
        user = session.get(User,id)
        return user