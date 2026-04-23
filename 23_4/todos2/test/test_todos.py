from .utils import *
from fastapi import status
import pytest
from models import Todos



def test_read_all_authenticated(test_todo):
    response = client.get("/")
    print(response.json()) 
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id':1,'title': 'Learn to code',
        'description' : 'Learn code everyday',
        'owner_id': 1,
        'priority': 5,
        'complete': False}]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    print(response.json()) 
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id':1,'title': 'Learn to code',
        'description' : 'Learn code everyday',
        'owner_id': 1,
        'priority': 5,
        'complete': False}


def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {'detail':"Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        'title':'New todo',
        'description':"New todo description",
        'priority':5,
        'complete':False
    }
    response = client.post("/todo/",json = request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.complete == request_data.get("complete")

def test_update_todo(test_todo):
    update_request = {
        'title':'change the title for todo',
        'description':'now to learn everydy',
        'priority':5,
        'complete':1
    }
    response = client.put("/todo/1",json = update_request)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'change the title for todo'


def test_update_todo_not_found(test_todo):
    update_request = {
        'title':'change the title for todo',
        'description':'now to learn everydy',
        'priority':5,
        'complete':1
    }
    response = client.put("/todo/99",json = update_request)
    assert response.status_code == 404


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/99")
    assert response.status_code == 404
    assert response.json() == {'detail':"todo id not found"}