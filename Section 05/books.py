# Swagger http://127.0.0.1:8000/docs
from fastapi import Body, FastAPI

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

# Add longer endpoints after shorter ones.
@app.get("/books/{book_title}/{book_author}/")
async def read_authors_for_book_title(book_title: str, book_author: str):
    ret = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('title').casefold() == book_title.casefold():
            ret.append(book)
    return ret



@app.post("/books")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)


@app.put("/books")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            
@app.delete("/books")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
            
            