from fastapi import FastAPI, Request
from models import Base
from database import engine
from router import auth,todos,admin,users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind = engine)

templates = Jinja2Templates(directory = 'templates')

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request : Request):
    return templates.TemplateResponse(name ='home.htm',request = request,context={"request": request})

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


# @app.get("/healthy")
# def status_check():
#     return {"status":"healthy"}