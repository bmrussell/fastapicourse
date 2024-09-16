from fastapi import FastAPI

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'maths'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'maths'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'maths'}
]

app = FastAPI()

# Static routes with no prameters should come first


@app.get("/books")
async def read_all_books():
    return BOOKS

# http://127.0.0.1:8000/books/?category=maths


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    ret = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            ret.append(book)
    return ret

# http://127.0.0.1:8000/books/Author%20Four/?category=science
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    ret = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            ret.append(book)
    return ret
