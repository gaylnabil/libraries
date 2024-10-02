from fastapi import FastAPI, HTTPException
from typing import List
from models import Book
from uuid import UUID, uuid4
from pymongo import MongoClient, AsyncMongoClient
import os
from dotenv import load_dotenv

load_dotenv()

async def connection():
    return await MongoClient(host, port)

host = os.environ.get('HOST', str)
port = int(os.environ.get('PORT'))

client = connection()
db = client.library

books = db.Books

app = FastAPI()


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


@app.post('/books', response_model=Book)
async def create_book(bk: Book):
    # bk.id = uuid4()
    book = books.insert_one(bk)
    return book

@app.put('/books/{book_id}', response_model_by_alias=Book)
async def update_book(book_id: UUID, book_updated: Book):
    
    for idx, bk in enumerate(books):
        if bk.id == book_id:
            book_updated = bk.copy(update=book_updated.dict(exclude_unset=True))
            books[idx] = book_updated
            return book_updated

    return HTTPException(status_code=404, detail=f'the book is not found')

@app.delete('/books/{id}')
async def delete_book(book_id: UUID):
    
    for bk in books:
        if bk.id == book_id:
            books.remove(bk)
            return books
            
    return HTTPException(status_code=404, detail=f'the book is not found')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)