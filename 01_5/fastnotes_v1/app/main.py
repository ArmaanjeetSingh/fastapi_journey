from fastapi import FastAPI,Depends
from app.notes import services as notes_services
from app.notes.schemas import *
from typing import List, Annotated
from app.db.config import get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

session_dependency = Annotated[AsyncSession,Depends(get_db)]

@app.post("/notes",response_model = NoteOut)
async def create_note(note_request : NoteCreate,session : session_dependency):
    # note = await notes_services.create_note(note_request['title'],note_request['content'])
    note = await notes_services.create_note(note_request,session)
    return note

@app.get("/notes/{note_id}",response_model=NoteOut)
async def get_notes(note_id : int,session : session_dependency):
    note = await notes_services.get_note(note_id,session)
    return note


@app.get("/notes/",response_model = List[NoteOut])
async def get_notes(session : session_dependency):
    note = await notes_services.get_all_notes(session)
    return note

@app.put("/notes/{note_id}",response_model=NoteOut)
async def update_note(note_id : int, new_note : NoteUpdate,session : session_dependency):
    # new_title = new_note.get("title")
    # new_content = new_note.get("content")
    # note = await notes_services.update_note(note_id,new_title,new_content)
    note = await notes_services.update_note(note_id,new_note,session)
    return note

@app.patch("/notes/{note_id}",response_model=NoteOut)
async def patch_note(note_id : int, new_note : NotePatch,session : session_dependency):
    # new_title = new_note.get("title")
    # new_content = new_note.get("content")
    # note = await notes_services.update_note(note_id,new_title,new_content)
    note = await notes_services.update_note(note_id,new_note,session)
    return note


@app.delete("/notes/{note_id}")
async def delete_note(note_id : int,session : session_dependency):
    note = await notes_services.delete_note(note_id,session)
    return note