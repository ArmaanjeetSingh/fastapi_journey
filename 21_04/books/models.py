from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)


class Books(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    rating = Column(Integer)
    is_available = Column(Boolean)

    owner_id = Column(Integer,ForeignKey("users.id"))

