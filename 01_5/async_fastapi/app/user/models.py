from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric
from app.db.base import Base

# class ProductModel(Base):
#     __tablename__ = 'products'

#     id : Mapped[int] = mapped_column(primary_key = True, index = True)
#     name : Mapped[str] = mapped_column(String(20),nullable = False)
#     price : Mapped[float] = mapped_column(Numeric,nullable = False)

#     def __repr__(self)->str:
#         return f"< Product(id = {self.id} name = {self.name} price = {self.price}) >"
class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key = True, index = True)
    name : Mapped[str] = mapped_column(String(20),nullable = False)
    email : Mapped[str] = mapped_column(String(20),nullable = False, unique = True)

    def __repr__(self)->str:
        return f"< User (id = {self.id} name = {self.name} email = {self.email}) >"