from .models import Base
from .database import engine
from fastapi import FastAPI, Request
from .routers import auth, expenses, category, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()


Base.metadata.create_all(bind = engine)
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(base_dir, "static")
app.mount("/static",StaticFiles(directory = static_path),name = 'static')
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(category.router)