from db import engine
from models import users, posts
from sqlalchemy import insert, delete, update, select


def create_user(name : str, email : str):
    with engine.connect() as conn:
        stmt = insert(users).values(name = name, email = email)
        conn.execute(stmt)
        conn.commit()


def create_post(title : str, content : str, user_id : int):
    with engine.connect() as conn:
        stmt = insert(posts).values(title = title,content =content, user_id = user_id)
        conn.execute(stmt)
        conn.commit()

def get_user_by_id(id : int):
    with engine.connect() as conn:
        stmt = select(users).where(users.c.id == id)
        result = conn.execute(stmt).first()
        print(result)


def get_all_users():
    with engine.connect() as conn:
        stmt = select(users)
        result = conn.execute(stmt).fetchall()
        print(result)


def get_posts_by_user(user_id : int):
    with engine.connect() as conn:
        stmt = select(posts).where(posts.c.user_id == user_id)
        result = conn.execute(stmt).fetchall()
        return result


def user_update_email(email : str, new_email : str):
    with engine.connect() as engine:
        stmt = update(users).where(users.c.email == email).values(email = email)
        conn.execute(stmt)
        conn.commit()