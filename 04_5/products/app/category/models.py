from app.db.base import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

class Category(Base):
    __tablename__ = 'category'

    id : Mapped[int] = mapped_column(primary_key=True,nullable = False, index = True)
    name : Mapped[str] = mapped_column(String, nullable = False)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")
