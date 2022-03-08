from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, max_length=50)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(
        title="Description of the book", max_length=100, min_length=1
    )
    rating: int = Field(gt=-1, lt=101)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "24e7a316-b611-4266-a0ba-0db86a7b6fe9",
                "title": "CS Pro",
                "author": "Nietszche",
                "description": "Nice book",
                "rating": 75
            }
        }

BOOKS = []

@app.get("/")
async def read_all_books(limit_books: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    if limit_books and len(BOOKS) >= limit_books > 0:
        i = 1
        new_books = []
        while i <= limit_books:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for book in BOOKS:
        if book.id == book_id:
            return book
    

@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    for i, x in enumerate(BOOKS):
        if x.id == book_id:
            BOOKS[i] = book
            return book


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    for i, x in enumerate(BOOKS):
        if x.id == book_id:
            del BOOKS[i]
            return f'BOOK {book_id} deleted!'
    raise HTTPException(status_code=404, detail="Book not found!", headers={"X-Header-Error": "Nothing to be seen at the UUID"})

def create_books_no_api():
    book_1 = Book(
        id="24e7a316-b611-4266-a0ba-0db86a7b6fe9",
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=10,
    )
    book_2 = Book(
        id="2d787865-2a58-4ca1-a6a9-d9a8ac209966",
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=50,
    )
    book_3 = Book(
        id="f0d940d2-deae-4447-a8ce-4ad14c1529ca",
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=100,
    )
    book_4 = Book(
        id="7783aef2-6af6-4848-a530-14b3c2a4cc91",
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=77,
    )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
