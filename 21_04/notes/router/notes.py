from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated, Optional
from models import Tags, Notes
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, computed_field
from datetime import datetime, timezone

class Note(BaseModel):
    title : str = Field(max_length = 30)
    content : str = Field(max_length = 50)
    
    @computed_field
    def created_at(self) -> str:
        return datetime.now(timezone.utc)

class NoteUpdate(BaseModel):
    title : str = Field(max_length = 30)
    content : str = Field(max_length = 50)

    @computed_field
    def updated_at(self)-> str:
        return datetime.now(timezone.utc)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try :
        yield db 
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]


@router.get("/get_all",status_code = status.HTTP_200_OK)
def get_all(db : db_dependency):
    return db.query(Notes).all()


@router.get("/get_tags/{note_id}",status_code = status.HTTP_200_OK)
def get_tags(db : db_dependency,note_id : int = Path(gt = 0)):
    notes_model = db.query(Notes).filter(Notes.id == note_id).first()
    if notes_model is None:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    print(repr(notes_model.tags))
    print(notes_model.tags)
    print(type(notes_model))
    return notes_model.tags


@router.get("/get_all/{note_id}",status_code = status.HTTP_200_OK)
def get_all(db : db_dependency, note_id : int = Path(gt = 0)):
    notes_model = db.query(Notes).filter(Notes.id == note_id).first()
    if notes_model is None:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    return notes_model



@router.post("/create_note",status_code =status.HTTP_201_CREATED)
def create_note(db : db_dependency, note : Note):
    note_model = Notes(**note.model_dump())
    print(note)
    print(note_model.created_at)
    db.add(note_model)
    db.commit()


@router.post("/create_note/{tag_id}",status_code =status.HTTP_201_CREATED)
async def create_note(db : db_dependency, note : Note, tag_id : int = Path(gt = 0)):
    tag_model = db.query(Tags).filter(Tags.id == tag_id).first()
    if tag_model is None :
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    note_model = Notes(**note.model_dump())
    note_model.tags.append(tag_model)
    print(type(note_model))
    print(type(note_model.tags))
    print(note_model)
    db.add(note_model)
    db.commit()


@router.put("/update_note/{note_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_note(db : db_dependency,note : NoteUpdate, note_id : int = Path(gt = 0)):
    note_model = db.query(Notes).filter(Notes.id == note_id).first()
    if not note_model:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    note_model.title = note.title
    note_model.content = note.content
    note_model.updated_at = note.updated_at
    db.add(note_model)
    db.commit()



@router.delete("/delete_note/{note_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_note(db : db_dependency,note_id : int = Path(gt = 0)):
    note_model = db.query(Notes).filter(Notes.id == note_id).first()
    if not note_model:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    db.delete(note_model)
    db.commit()


