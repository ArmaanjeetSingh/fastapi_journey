from fastapi import FastAPI
import models
from database import engine
from router import notes,tags,auth

models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(notes.router)
app.include_router(tags.router)
app.include_router(auth.router)