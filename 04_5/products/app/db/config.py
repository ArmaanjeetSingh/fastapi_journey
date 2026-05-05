from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = os.path.join(BASE_DIR,"testdb.db")

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo = True)

SessionLocal = sessionmaker(bind = engine, expire_on_commit= False)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]
