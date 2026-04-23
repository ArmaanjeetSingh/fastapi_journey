from .utils import *
from router.admin import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/todo")
    print(response.json())
    # assert response.status_code == status.HTTP_200_OK
    # assert response.json() == [{'id':1,'title': 'Learn to code',
    #     'description' : 'Learn code everyday',
    #     'owner_id': 1,
    #     'priority': 5,
    #     'complete': False}]
