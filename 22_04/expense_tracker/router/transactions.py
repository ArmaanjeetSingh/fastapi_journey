from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from database import SessionLocal,engine
from models import Category, Transactions
from typing import Annotated, Literal, Optional
from .users import get_current_user
from datetime import datetime
from datetime import timezone
from pydantic import BaseModel, Field, computed_field
from .categories import get_category_by_id

class TransactionRequest(BaseModel):
    amount : float
    type : str
    category_id: int
    description : str

    @computed_field
    def created_at(self) -> str:
        return datetime.now(timezone.utc).strftime("%d-%m-%y")

class TransactionUpdateRequest(BaseModel):
    amount : float
    type : str
    category_id: int
    description : str


router = APIRouter(
    prefix = '/transactions',
    tags = ['transactions']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
# category_dependency = Annotated[]


@router.post("/",status_code = status.HTTP_201_CREATED)
async def create_transaction(transaction_request : TransactionRequest, db : db_dependency, user : user_dependency):
    transaction_request_model = Transactions(**transaction_request.model_dump())
    transaction_request_model.user_id = user.get("id")
    db.add(transaction_request_model)
    db.commit()


@router.get("/",status_code = status.HTTP_200_OK)
async def get_transaction(db : db_dependency, user : user_dependency,type : Optional[str] = None,category : Optional[str] = None):
    transaction_model = db.query(Transactions).filter(user.get("id") == Transactions.user_id).all()
    if transaction_model is None:
        raise HTTPException(status_code = 404, detail = 'no transaction found')
    transac_to_return = []
    for transac in transaction_model:
        category_transac = await get_category_by_id(transac.id,user,db)
        print(category_transac.type)
        if type is not None and  transac.type.casefold() != type.casefold():
            continue
        if category is not None and category_transac.type.casefold() != category.casefold():
            continue
        transac_to_return.append(transac)
    return transac_to_return


@router.get("/{id}",status_code = status.HTTP_200_OK)
async def get_transaction_by_id(id : int,db : db_dependency, user : user_dependency):
    transaction_model = db.query(Transactions).filter(user.get("id") == Transactions.user_id).filter(id == Transactions.id).first()
    if transaction_model is None:
        raise HTTPException(status_code = 404, detail = 'no transaction found')
    return transaction_model


@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_transaction(id : int,db : db_dependency, user : user_dependency):
    transaction_model = db.query(Transactions).filter(user.get("id") == Transactions.user_id).filter(id == Transactions.id).first()
    if transaction_model is None:
        raise HTTPException(status_code = 404, detail = 'no transaction found')
    db.delete(transaction_model)
    db.commit()



@router.put("/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def update_transaction(id : int,db : db_dependency, user : user_dependency, update_transaction : TransactionUpdateRequest):
    transaction_model = db.query(Transactions).filter(user.get("id") == Transactions.user_id).filter(id == Transactions.id).first()
    if transaction_model is None:
        raise HTTPException(status_code = 404, detail = 'no transaction found')
    transaction_model.description = update_transaction.description
    transaction_model.amount = update_transaction.amount
    transaction_model.type = update_transaction.type
    transaction_model.category_id = update_transaction.category_id
    db.add(transaction_model)
    db.commit()