from app.notes.models import Notes
from sqlalchemy import select
from fastapi import HTTPException
from app.notes.schemas import NoteUpdate, NotePatch, NoteCreate, NoteOut
from sqlalchemy.ext.asyncio import AsyncSession

async def create_note(new_note : NoteCreate, session : AsyncSession) -> NoteOut:
    note = Notes(title = new_note.title, content = new_note.content)
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note


async def get_note(note_id : int,session : AsyncSession) -> NoteOut:
    note = await session.get(Notes,note_id)
    if note is None:
        raise HTTPException(status_code = 404, detail = 'notes not found')
    return note


async def get_all_notes(session : AsyncSession) -> NoteOut:
    stmt = select(Notes)
    notes = await session.scalars(stmt).all()
    return notes


async def update_note(note_id : int,new_note : NoteUpdate,session : AsyncSession) -> NoteOut:
    note = await session.get(Notes,note_id)
    if note is None:
        raise HTTPException(status=404,detail = f'note not found')
    note.title = new_note.title
    note.content = new_note.content
    await session.commit()
    await session.refresh(note)
    return note



async def patch_note(note_id : int,new_note : NotePatch,session : AsyncSession) -> NoteOut:
    note = await session.get(Notes,note_id)
    if note is None:
        raise HTTPException(status=404,detail = f'note not found')
    update_data = new_note.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    await session.commit()
    await session.refresh(note)
    return note



async def delete_note(note_id,session : AsyncSession):
    note = await session.get(Notes,note_id)
    if note is None:
        raise HTTPException(status=404,detail = f'note not found')
    await session.delete(note)
    await session.commit()
    return {"message":"deleted"}
