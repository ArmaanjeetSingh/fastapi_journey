from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated, Optional
from models import Tags, Notes,note_tag
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, computed_field
from datetime import datetime, timezone

class Tag(BaseModel):
    title : str = Field(max_length = 50)

router = APIRouter(
   prefix = '/tags',
   tags = ['tags']
)

def get_db():
    db = SessionLocal()
    try :
        yield db 
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]
@router.get("/get_all_tags",status_code = status.HTTP_200_OK)
async def get_all_tags(db : db_dependency):
    return db.query(Tags).all()


@router.post("/create_tag", status_code = status.HTTP_201_CREATED)
async def create_tag(tag : Tag, db : db_dependency):
    new_tag = Tags(**tag.model_dump())
    db.add(new_tag)
    db.commit()


@router.put("/update_tag/{tag_id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_tag(db : db_dependency, tag : Tag, tag_id : int):
    tag_model = db.query(Tags).filter(Tags.id == tag_id).first()
    if tag_model is None:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    tag_model.title = tag.title
    db.add(tag_model)
    db.commit()


@router.delete("/delete_tag/{tag_id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_tag(db : db_dependency, tag_id : int):
    tag_model = db.query(Tags).filter(Tags.id == tag_id).first()
    if tag_model is None:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    db.delete(tag_model)
    db.commit()


# Attach tag to note
@router.post("/attach_tag/{tag_id}/{note_id}",status_code = status.HTTP_201_CREATED)
async def attach_tag(db : db_dependency,tag_id : int, note_id : int):
    tag_model = db.query(Tags).filter(Tags.id == tag_id).first()
    notes_model = db.query(Notes).filter(Notes.id == note_id).first()
    print(tag_model)
    print(notes_model)
    if tag_model is None or notes_model is None:
        raise HTTPException(status_code = 404, detail = f'no such ID found')
    if tag_model in notes_model.tags:
        return {"message": "Tag already attached to this note"}

    notes_model.tags.append(tag_model)
    db.add(notes_model)
    db.commit()
    return {"message": "Tag attached successfully"}
