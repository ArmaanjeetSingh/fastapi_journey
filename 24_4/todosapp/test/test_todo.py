from router.todos import get_current_user,get_db
from fastapi import status
from models import Base, Todos, Users
import pytest 
from .utils import *



app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/todos/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title":"Learn to code","description":"Need to learn everyday","complete":False,"priority":5,"owner_id":3, "id":1}]
    

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"title":"Learn to code","description":"Need to learn everyday","complete":False,"priority":5,"owner_id":3, "id":1}


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/todo/100")
    assert response.status_code == 404
    assert response.json() == {"detail":"no todo found"}

def test_create_todo_authenticated(test_todo):
    request_data = {
        'title' : "Learn new thing",
        'description' : 'Learn everyday for creativity',
        'priority' : 5,
        'complete' : False
    }
    response = client.post("/todos/todo",json = request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        'title' : "Learn new thing together",
        'description' : 'Learn C++',
        'priority' : 5,
        'complete' : True
    }
    db = TestingSessionLocal()
    response = client.put("/todos/todo/1",json = request_data)
    assert response.status_code == 204
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get("title")


def test_update_todo_not_found(test_todo):
    request_data = {
        'title' : "Learn new thing together",
        'description' : 'Learn C++',
        'priority' : 5,
        'complete' : True
    }
    db = TestingSessionLocal()
    response = client.put("/todos/todo/99",json = request_data)
    assert response.status_code == 404


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail":'no todo found'}