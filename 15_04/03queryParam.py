from fastapi import FastAPI

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