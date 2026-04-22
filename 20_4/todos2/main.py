from fastapi import FastAPI
from typing import Annotated
import models
from models import Todos
from database import engine, SessionLocal

from router import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)


