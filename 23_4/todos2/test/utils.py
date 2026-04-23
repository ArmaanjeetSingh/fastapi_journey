from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models import Base, Todos, Users
from router.todos import get_current_user,get_db
import pytest
from fastapi.testclient import TestClient 
from main import app
from router.auth import bcrypt_context

SQLALCHMEY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHMEY_DATABASE_URL,
    connect_args={'check_same_thread':False},
    poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)
Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try : 
        yield db

    finally:
        db.close()

def override_get_current_user():
    return {'username':'armaan','id':1,'role':'admin'}


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos (
        title = 'Learn to code',
        description  = 'Learn code everyday',
        owner_id = 1,
        priority = 5,
        complete = False
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
    db.close()



@pytest.fixture
def test_user():
    user = Users(
        username = 'armaan',
        email = 'armaan12@gmail.com',
        first_name = 'armaan',
        last_name = 'singh',
        hashed_password = bcrypt_context.hash('1234'),
        role = 'admin'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect()  as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
        