from database import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

note_tag = Table(
    "note_tag",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean)
    role = Column(String)
    phone_number = Column(String,nullable=True)


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

    notes = relationship("Notes", secondary=note_tag, back_populates="tags")


class Notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    created_at = Column(String, nullable=False)
    updated_at = Column(String)

    tags = relationship("Tags", secondary=note_tag, back_populates="notes")
    owner_id = Column(Integer,ForeignKey("users.id"))