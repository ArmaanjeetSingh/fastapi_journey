from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from models import Base, Todos, Users
import pytest 
from router.auth import bcrypt_context

from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {'check_same_thread':False},
    poolclass = StaticPool   
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind =  engine)

Base.metadata.create_all(engine)


def override_get_db():
    db = TestingSessionLocal()
    try :
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'armaantest','id':1,"role":'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code",
        description = "Need to learn everyday",
        priority = 5,
        complete = False,
        owner_id = 3
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = 'armaantest1',
        email = 'arm12345@gmail.com',
        first_name = 'armaan',
        last_name = 'singh',
        hashed_password = bcrypt_context.hash('123'),
        role = 'admin',
        phone_number = '1234567890',
        is_active = True
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()