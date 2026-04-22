from fastapi import FastAPI
from models import Base
from database import engine
from router import categories,users,transactions

app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(transactions.router)