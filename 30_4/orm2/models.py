from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy import String
from typing import List
from db import engine

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(20), nullable = False)
    email : Mapped[str] = mapped_column(String, nullable = False, unique = True)

    posts: Mapped[list["Post"]] = relationship("Post",back_populates = 'user',cascade = 'all,delete') #two way relationship

    #one -to -one
    posts : Mapped["Profile"] = relationship("Profile",back_populates = "user",uselist = False, cascade = "all,delete")

    #many to many
    address : Mapped[List["Address"]] = relationship("Address",back_populates = "user",uselist = False, cascade = "all,delete")

    def __repr__(self) -> str:
        return f"<User(id = {self.id}, name = {self.name}, email = {self.email})>"


#one to many
class Post(Base):
    __tablename__ = 'posts'

    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id",ondelete = 'CASCADE'),nullable = False,unique = True)
    title : Mapped[str] = mapped_column(String(20), nullable = False)
    content : Mapped[str] = mapped_column(String, nullable = False)

    user: Mapped["User"] = relationship("User",back_populates = 'posts')

    def __repr__(self) -> str:
        return f"<Post (id = {self.id}, name = {self.title}, email = {self.content})>"


#many to many
class Address(Base):
    __tablename__ = 'addresses'

    id : Mapped[int] = mapped_column(primary_key = True)
    street : Mapped[str] = mapped_column(String(50),nullable=False)
    dist : Mapped[str] = mapped_column(String,nullable = False)
    country : Mapped[str] = mapped_column(String,nullable = False)

    users : Mapped["User"] = relationship("User",back_populates = 'addresses')

    def __repr__(self)->str:
        return f"Address (id = {self.id!r},street = {self.street!r})"

user_address_association = Table(
    "user_address_association",
    Base.metadata,
    Column("user_id",Integer,ForeignKey("users.id",ondelete = "CASCADE"),primary_key = True),
    Column("address_id",Integer,ForeignKey("addresses.id",ondelete = "CASCADE"),primary_key = True)
)
#Create table
def create_tables():
    Base.metadata.create_all(engine)