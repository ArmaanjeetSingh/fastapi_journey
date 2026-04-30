from fastapi import APIRouter, status, HTTPException, Depends
from .auth import get_current_user
from ..database import SessionLocal
from ..models import Expenses
from typing import Annotated, Optional
from sqlalchemy.orm import Session 
from pydantic import BaseModel, computed_field
from datetime import datetime
from datetime import datetime, timezone

class ExpenseRequest(BaseModel):
    amount : float
    type : str
    category_id : int

    @computed_field
    def created_at(self)->str:
        return datetime.now(timezone.utc)


class ExpenseUpdate(BaseModel):
    amount : Optional[float] = None
    type : str
    category_id : Optional[int] = None


router = APIRouter(
    prefix = '/expenses',
    tags = ['expenses']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/",status_code = status.HTTP_201_CREATED)
async def create_expense(create_expense_request : ExpenseRequest, db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')
    create_expense_model = Expenses(
        amount = create_expense_request.amount,
        user_id = user.get("id"),
        type = create_expense_request.type,
        created_at = create_expense_request.created_at,
        category_id = create_expense_request.category_id,
    )
    db.add(create_expense_model)
    db.commit()


@router.get("/",status_code = status.HTTP_200_OK)
async def get_expenses(db : db_dependency, user : user_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')
    expenses_model = db.query(Expenses).filter(user.get("id") == Expenses.user_id).all()
    if not expenses_model:
        raise HTTPException(status_code = 404, detail = 'not found')
    return expenses_model


@router.get("/{id}",status_code = status.HTTP_200_OK)
async def get_expenses_by_id(db : db_dependency, user : user_dependency,id : int):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')
    expenses_model = db.query(Expenses).filter(user.get("id") == Expenses.user_id).filter(Expenses.id == id).first()
    if not expenses_model:
        raise HTTPException(status_code = 404, detail = 'not found')
    return expenses_model


@router.put("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_expenses(db : db_dependency, user : user_dependency,id : int, update_expense_request : ExpenseUpdate):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')
    expenses_model = db.query(Expenses).filter(user.get("id") == Expenses.user_id).filter(Expenses.id == id).first()
    if not expenses_model:
        raise HTTPException(status_code = 404, detail = 'not found')
    update_data = update_expense_request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(expenses_model,key,value)
    db.add(expenses_model)
    db.commit()


@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_expenses(db : db_dependency, user : user_dependency,id : int):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'not authenticated user')
    expenses_model = db.query(Expenses).filter(user.get("id") == Expenses.user_id).filter(Expenses.id == id).first()
    if not expenses_model:
        raise HTTPException(status_code = 404, detail = 'not found')
    db.delete(expenses_model)
    db.commit()