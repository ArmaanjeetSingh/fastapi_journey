from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key = True, index = True)
    name = Column(String, unique = True)
    email = Column(String)
    hashed_password = Column(String)
    role = Column(String, nullable = False)
    transactions = relationship("Expenses",back_populates = 'user')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer,primary_key = True, index = True)
    name = Column(String)
    description = Column(String)


class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer,primary_key = True, index = True)
    amount = Column(Numeric,nullable = False)
    type = Column(String, nullable = False)
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String)
    user = relationship("Users", back_populates="transactions")
