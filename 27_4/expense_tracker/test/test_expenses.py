from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from expense_tracker.database import Base
from expense_tracker.main import app
from expense_tracker.routers.expenses import get_db, get_current_user
from fastapi.testclient import TestClient
import pytest
from expense_tracker.models import Expenses
from fastapi import status


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args = {'check_same_thread':False}, poolclass = StaticPool)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base.metadata.create_all(bind = engine)
def override_get_db():
    db = TestingSessionLocal()
    try :
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'armaan12','id':1,'role':'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_expense():
    expense = Expenses(
        amount = 125,
        type = 'income',
        category_id = 1,
        user_id = 1,
        created_at = '23-04-2026'
    )
    db = TestingSessionLocal()
    db.add(expense)
    db.commit()
    yield expense
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM expenses;"))
        connection.commit()


def test_read_all_authenticated(test_expense):
    response = client.get("/expenses")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id":1,"amount":125.0,"category_id": 1,"user_id": 1,
        "created_at":'23-04-2026','type':'income'
    }]


def test_read_one_authenticated(test_expense):
    response = client.get("/expenses/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id":1,"amount":125.0,"category_id": 1,"user_id": 1,
        "created_at":'23-04-2026','type':'income'
    }



def test_create_expense(test_expense):
    request_data  = {
        "amount":125.0,"category_id": 1,'type':'income'
    }
    responses = client.post("/expenses",json = request_data)
    assert responses.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    model = db.query(Expenses).filter(Expenses.id == 2).first()
    assert model.amount == request_data.get('amount')
    assert model.type == request_data.get('type')


def test_update_expense(test_expense):
    request_data = {
        'amount':100,'category_id':2,'type':'expense'
    }
    response = client.put("/expenses/1",json = request_data)
    print(response)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Expenses).filter(Expenses.id == 1).first()
    assert model.amount == request_data.get('amount')


def test_update_expense(test_expense):
    request_data = {
        'amount':100,'category_id':2,'type':'expense'
    }
    response = client.put("/expenses/99",json = request_data)
    assert response.status_code == 404


def test_delete_todo(test_expense):
    response = client.delete("/expenses/1")
    assert response.status_code == 204