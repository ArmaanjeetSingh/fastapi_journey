from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory = 'templates')

posts : list[dict] = [
    {
        "id":1,
        "author":"Rabindranath Tagore",
        "title":"Gitanjali",
        "description":"awesome book of peotry",
        "date_posted":"April 19, 1925"
    },
    {
        "id":2,
        "author":"Jane Doe",
        "title":"FastAPI is awesome",
        "description":"This framework is really easy to use and super fast",
        "date_posted":"April 21, 1987"
    }
]

@app.get("/posts",include_in_schema = False)
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",{"posts":posts, "title":"Home"})
