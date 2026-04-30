from fastapi import FastAPI, status, Query, Path
from pydantic import BaseModel, EmailStr, Field, AfterValidator
from typing import Annotated, Optional

import random

class Book(BaseModel):
    title : Annotated[str,Field(max_length=50)]
    author : Optional[Annotated[str,Field(max_length=50)]] = "anonymous"
    published_year: Annotated[int,Field(lt = 2023, ge = 1920)]
    rating : Annotated[float,Field(gt = 0, lt = 5)]

BOOKS = [
    {"title":"Gitanjali","author":"Rabindranath Tagore","isbn":"bn-1234","published_year":1925,"rating":4.2},
    {"title":"Chronicles of Narniya","author":"O G Cromwell","isbn":"bn-1232","published_year":1986,"rating":3.9},
    {"title":"The Paradise","author":"J K williams","isbn":"bn-1247","published_year":1995,"rating":3.8},
    {"title":"Curse of Twilight","author":"R K Manon","isbn":"bn-1345","published_year":1971,"rating":2.7},
    {"title":"Blooming youth","author":"Harry Potsherd","isbn":"bn-1237","published_year":1983,"rating":4.0},
]
def check_valid_id(isbn_no):
    if not isbn_no.startswith("bn-"):
        raise ValueError("invalid id format")
    return isbn_no

app = FastAPI()

@app.get("/books")
def get_book(title : Annotated[str|None,Field(max_length = 50)] = None,min_rating : Annotated[float|None,Field(gt = 0, lt = 5)] = None, year_gt : Annotated[int|None,Field(lt = 2023, ge = 1920)] = None):
    filtered_books = []
    for book in BOOKS:
        if title is not None and title.lower() not in book.get("title").lower():
            continue
        if min_rating is not None and min_rating > book.get("rating"):
            continue
        if year_gt is not None and year_gt > book.get("published_year"):
            continue
        filtered_books.append(book)
    return filtered_books

@app.get("/books/{isbn_no}")
def get_book_by_isbn(isbn_no : Annotated[str,AfterValidator(check_valid_id)]):
    for book in BOOKS:
        if isbn_no in book.get("isbn"):
            return book
    return {"message":"no such book found"}

@app.post("/books")
def create_book(create_book_request : Book):
    create_book_model = create_book_request.model_dump()
    create_book_model["id"] = "bn-"+str(random.randint(1000,2000))
    BOOKS.append(create_book_model)