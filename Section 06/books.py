from typing import Annotated, Optional

from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publication_year: int
    
    def __init__(self, id, title, author, description, rating, publication_year) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publication_year = publication_year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID not needed on create', default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    publication_year: int = Field(gt=0, lt=3000)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Model Village",
                "author": "Aaron Aaronsen",
                "description": "A big cop's real home",
                "rating": 5,
                "publication_year": 1998
            }
        }
    }
    
BOOKS = [
    Book(1, 'Computer Science Pro', 'Alice Aaronsen', 'Advanced CS', 5, 1998),
    Book(2, 'The Python Handbook', 'John Smith', 'Comprehensive guide to Python', 2, 1998),
    Book(3, 'Algorithms Unlocked', 'Charles Lee', 'In-depth exploration of algorithms', 4, 2000),
    Book(4, 'Data Structures Demystified', 'Emma Brown', 'Simplifying data structures', 3, 2001),
    Book(5, 'AI: The New Frontier', 'Sophia Davis', 'Introduction to artificial intelligence', 4, 2000),
    Book(6, 'Deep Learning with Python', 'Michael Johnson', 'Comprehensive introduction to deep learning concepts using Python', 6, 2003)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def read_book(id: int = Path(gt=0)):  # Path validation {id} must be > 0
    for book in BOOKS:
        if book.id == id:
            return book

    raise HTTPException(status_code=404, detail="Book cannot be found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating_or_publication_year(rating: Annotated[int | None, Query(gt=0, lt=6)] = None, publication_year: Annotated[int | None, Query(gt=0, lt=3000)] = None):
    # Parameters defaulted to None (optional) with validations
    book_return = []
    
    if rating == None and publication_year == None:
        return book_return
    
    for book in BOOKS:
        if (rating == None or book.rating == rating) and (publication_year == None or book.publication_year == publication_year):
            book_return.append(book)
    
    return book_return

def get_next_book_id():   
    bookid = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return bookid

@app.post("/books", status_code=status.HTTP_201_CREATED) # Return HTTP 201 CREATED by default
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book.id = get_next_book_id()
    BOOKS.append(new_book)
    
@app.put("/books/{id}", status_code=status.HTTP_204_NO_CONTENT) # Return HTTP 204 NO CONTENT by default
async def update_a_book(id: int = Path(gt=0), book_request: BookRequest = None):
    for book in BOOKS:
        if book.id == id:
            book.author = book_request.author
            book.title = book_request.title
            book.description = book_request.description
            book.rating = book_request.rating
            book.publication_year = book_request.publication_year
            return
    
    raise HTTPException(status_code=404, detail="Book cannot be found")

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT) # Return HTTP 204 NO CONTENT by default)
async def delete_a_book(id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            return
    
    raise HTTPException(status_code=404, detail="Book cannot be found")