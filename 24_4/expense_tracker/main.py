from .models import Base
from .database import engine
from fastapi import FastAPI
from .routers import auth, expenses, category

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific URL
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind = engine)


app.include_router(auth.router)
app.include_router(expenses.router)
app.include_router(category.router)