from sqlalchemy import Column,Boolean, String, Integer, Numeric, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key = True, index = True)
    name = Column(String, nullable = False, unique = True)
    email = Column(String, nullable = False, unique = True)
    hashed_password = Column(String)

    transactions = relationship("Transactions",back_populates = 'user')

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer,primary_key = True, index = True)
    name = Column(String, nullable = False)
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class Transactions(Base):
    __tablename__ = 'transactions'

    id = Column(Integer,primary_key = True, index = True)
    amount = Column(Numeric)
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer,ForeignKey("category.id"))
    description = Column(String, nullable = True)
    created_at = Column(String, nullable = True)

    user = relationship("Users", back_populates="transactions")