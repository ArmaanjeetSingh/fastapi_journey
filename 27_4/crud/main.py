from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import models
from database import engine,sessionlocal
from sqlalchemy.orm import Session 
from typing import Annotated

models.Base.metadata.create_all(bind = engine)

templates = Jinja2Templates(directory = 'templates')

app = FastAPI()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/")
def home(request : Request, db : db_dependency):
    users =  db.query(models.User).all()
    return templates.TemplateResponse(      
    {"users":users},
    request=request, 
    name="index.html", 
    context={}, 
)

@app.post("/add")
async def add(request : Request,db:db_dependency,name : str = Form(...), position : str = Form(...), office : str = Form()):
    user = models.User(name = name, position = position, office = office)
    print(user)
    db.add(user)
    db.commit()
    return RedirectResponse(url = app.url_path_for("home"),status_code = 303)


@app.get("/addnew")
async def addnew(request : Request):
    return templates.TemplateResponse(name = 'addnew.html',context = {},request = request)