from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()

class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date : int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id : Optional[int] = Field(description='ID is not on create', default=None)
    title : str = Field(min_length=10)
    author : str = Field(min_length=10)
    description : str = Field(min_length=1, max_length=50)
    rating : int = Field(gt=0, lt=6)
    published_date : int = Field(gt=1980,l=2036)

BOOKS = [
    Book(1,"Computer Science Pro","codebythroby","A very nice book",5,1998),
    Book(2,"Curse of 1800","George K.","thriller book",5,2002),
    Book(3,"Legend of Naarniya","Thomas Bombardy","A very nice book",3,1998),
    Book(4,"Jungle Book","Rudyard Kipling","A fascinaing journey of human living among animals",4,1990),
    Book(5,"Gitanjali","Rabindranath Tagore","A very nice book including beautiful poetry",5,2010),
    Book(6,"Be faster with FastAPI","codebythroby","A coding book",1,2010)
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/publish")
async def read_book_by_publish(published_date : Optional[int] = Query(gt = 1980, lt = 2036, default = None)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return 


@app.get("/books/{book_id}")
async def read_book_by_id(book_id:int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books")
async def read_book_by_rating(rating : Optional[int] = Query(gt = 0, lt = 6, default = None)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return 



@app.post("/create-book")
async def create_book(book_request : BookRequest):
    print(type(book_request))
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(book_request))


@app.put("/update-book")
async def update_book(book_request : BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request


@app.delete("/delete-book/{book_id}")
async def delete_book(book_id : int = Path(gt = 0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break




def find_book_id(book:Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    book.id = BOOKS[-1].id + 1 if BOOKS else 1
    return book