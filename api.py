from fastapi import FastAPI, HTTPException
from typing import List
from models import Book
from uuid import UUID, uuid4
app = FastAPI()

books = []
@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.get('/books/{book_id}', response_model_by_alias=Book)
async def retrieve_book(book_id: UUID):

    for bk in books:
        if bk.id == book_id:
            return bk

    return HTTPException(status_code=404, detail=f'the book is not found')
    
@app.get("/books", response_model=List[Book])
async def get_books():
    return books

