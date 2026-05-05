from sqlmodel import SQLModel, Field, Relationship
from pydantic import computed_field
from typing import List

class Product(SQLModel,table = True):
    id : int = Field(primary_key = True)
    quantity : int
    price : float
    user_id : int = Field(foreign_key="user.id",ondelete= 'CASCADE')

    user : List["User"] = Relationship(back_populates = 'orders')

    @computed_field(repr = False)
    @property
    def total_price(self)->float:
        if self.quantity is not None and self.price is not None:
           return self.quantity * self.price
        return 0.0


class ProductBase(SQLModel):
    quantity : int
    price : float 
    user_id : int
    @computed_field
    @property
    def total_price(self)->float:
        if self.quantity is not None and self.price is not None:
           return self.quantity * self.price
        return 0.0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id : int