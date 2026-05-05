from app.db.base import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped,relationship
from typing import Optional

class Product(Base):
    __tablename__ = 'product'

    id : Mapped[int] = mapped_column(primary_key=True,nullable = False, index = True)
    name : Mapped[str] = mapped_column(String, nullable = False)
    price : Mapped[float] = mapped_column(nullable = False)
    stock : Mapped[int] = mapped_column(nullable = False)

    category_id : Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")