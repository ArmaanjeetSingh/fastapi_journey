from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, BaseModel
from typing import List

class User(SQLModel,table = True):
    id : int = Field(primary_key = True)
    name : str
    email : str

    orders : List["Product"] = Relationship(back_populates = 'user')


class UserBase(BaseModel):
    name : str
    email : EmailStr


class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id : int

