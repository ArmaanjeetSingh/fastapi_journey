from pydantic import BaseModel, ConfigDict

class NoteBase(BaseModel):
    title : str
    content : str

class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass

class NotePatch(BaseModel):
    title : str | None = None
    content : str | None = None

class NoteOut(NoteBase):
    id : int
    model_config = ConfigDict(from_attributes = True)
