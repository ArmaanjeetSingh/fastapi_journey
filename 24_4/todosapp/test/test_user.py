from .utils import *
from router.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == 200
    assert response.json()['username'] == 'armaantest1'
    assert response.json()['email'] == 'arm12345@gmail.com'
    assert response.json()['first_name'] == 'armaan'
    assert response.json()['last_name'] == 'singh'


def test_change_password_success(test_user):
    response = client.put("/user/password",json = {"password":'123','new_password':'1234'})
    assert response.status_code == 204


def test_change_password_success_invalid(test_user):
    response = client.put("/user/password",json = {"password":'123567890','new_password':'1234'})
    assert response.status_code == 401