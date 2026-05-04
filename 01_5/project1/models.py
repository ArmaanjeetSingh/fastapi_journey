from db import Base, engine
from sqlalchemy.orm import mapped_column, Mapped,relationship
from sqlalchemy import String, Integer
from typing import List


class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    name : Mapped[str] = mapped_column(String(20),nullable = False)
    email : Mapped[str] = mapped_column(String,nullable = False,unique = True)
    phone : Mapped[int] = mapped_column(Integer,nullable = False,unique = True)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user", cascade="all, delete")

    def __repr__(self)->str:
        return f"< User (id = {self.id} name = {self.name} email = {self.email}) phone = {self.phone}>"


class Post(Base):
    __tablename__ = 'posts'

    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    title : Mapped[str] = mapped_column(String, nullable = False)
    content : Mapped[str] = mapped_column(String,nullable = False)
    owner_id : Mapped['User'] = relationship("User", back_populates='posts')

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title})>"


def create_table():
    Base.metadata.create_all(engine)