from fastapi import FastAPI, Body
from typing import Optional

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_books(category: str = None):
    if category:
        return [book for book in BOOKS if book['category'].casefold() == category.casefold()]
    return BOOKS


# Get book by title
@app.get("/books/title/{book_title}")
async def get_book_by_title(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}


# Get books by author and category
@app.get("/books/author/{author_name}")
async def get_books_by_author(author_name: str, category: str = None):
    result = []
    for book in BOOKS:
        if book['author'].casefold() == author_name.casefold():
            if category:
                if book['category'].casefold() == category.casefold():
                    result.append(book)
            else:
                result.append(book)
    return result



@app.post("/add_book")
def add_book(new_book = Body()):
    print(new_book)
    BOOKS.append(new_book)

@app.put("/books/update_book/")
async def update_book(updated_book =  Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book
            print(BOOKS[i])


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title : str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters.
@app.get("/books/fetch_all_books/{book_author}")
async def fetch_all_books(book_author: str, category: Optional[str] = None, book_title : Optional[str] = None):
    books_to_return = []
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() != book_author.casefold():
            continue
        if category is not None and BOOKS[i].get('category').casefold() != category.casefold():
            continue
        if book_title is not None and BOOKS[i].get('book_title').casefold() != book_title.casefold():
            continue
        print(BOOKS[i])
        books_to_return.append(BOOKS[i])
    return books_to_return