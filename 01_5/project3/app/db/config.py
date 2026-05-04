from sqlalchmy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = os.path.join(BASE_DIR,'sqlitedb.db')

DATABASE_URL = f'sqlite:///{db_path}'

engine = create_engine(DATABASE_URL,connect_args = {'check_same_thread':False})

SessionLocal = sessionmaker(bind = engine, expire_on_commit = False)
