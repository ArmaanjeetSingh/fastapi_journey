from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    name = Column(String(20))
    position = Column(String(80))
    office = Column(String(20))

    def __repr__(self):
        return '<User %r >'%(self.id)