from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    
BOOKS = [
    Book(1, 'Computer Science Pro', 'Alice Aaronsen', 'Advanced CS', 5),
    Book(2, 'The Python Handbook', 'John Smith', 'Comprehensive guide to Python', 2),
    Book(3, 'Algorithms Unlocked', 'Charles Lee', 'In-depth exploration of algorithms', 4),
    Book(4, 'Data Structures Demystified', 'Emma Brown', 'Simplifying data structures', 3),
    Book(5, 'AI: The New Frontier', 'Sophia Davis', 'Introduction to artificial intelligence', 4),
    Book(6, 'Deep Learning with Python', 'Michael Johnson', 'Comprehensive introduction to deep learning concepts using Python', 6)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book.id = get_next_book_id()
    BOOKS.append(new_book)
    
def get_next_book_id():   
    bookid = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return bookid