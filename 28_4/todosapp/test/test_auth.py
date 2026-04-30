from .utils import *
from router.auth import get_db, get_authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import datetime
from datetime import timedelta

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = get_authenticate_user(test_user.username,'123',db)
    assert authenticated_user is not None
    assert authenticated_user.username == 'armaantest1'

    non_exist_authenticated_user = get_authenticate_user('exampleuser1','123',db)
    assert non_exist_authenticated_user is False

    wrong_password_authenticated_user = get_authenticate_user(test_user.username,'123456789',db)
    assert wrong_password_authenticated_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days = 1)

    token = create_access_token(username,role,user_id,expires_delta)

    decode_token = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])

    assert decode_token['sub'] == username