from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from app.db.base import Base


class Notes(Base):
    __tablename__ = 'notes'

    id : Mapped[int] = mapped_column(primary_key = True)
    title : Mapped[str] = mapped_column(String)
    content : Mapped[str] = mapped_column(Text)