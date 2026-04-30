from fastapi import FastAPI, Request
from models import Base
from database import engine
from router import auth,todos,admin,users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

Base.metadata.create_all(bind = engine)

templates = Jinja2Templates(directory = 'templates')

import os
base_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(base_dir, "static")
app.mount("/static",StaticFiles(directory = static_path),name = 'static')


@app.get("/")
def test (request : Request):
    return templates.TemplateResponse(name ='home.htm',request = request, context = {})

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


# @app.get("/healthy")
# def status_check():
#     return {"status":"healthy"}