from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

DB_URL = 'sqlite:///./crud.sqlite3'

engine = create_engine(DB_URL,connect_args = {'check_same_thread':False})
sessionlocal = sessionmaker(autocommit = False,autoflush = False, bind = engine)
class Base(DeclarativeBase):
    pass