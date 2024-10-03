from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from models.book import Book
from schemas.entity import book_entity, books_entity
from models.configurations import books

book_router = APIRouter()

@book_router.get('/books/{book_id}')
async def retrieve_book(book_id: str):
    
    try:
        if data := books.find_one(ObjectId(book_id)):
            return book_entity(data)

        else:
            raise HTTPException(status_code=404, detail='The book is not found')
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Error: {e}') from e
    
@book_router.get("/books/")
async def get_books():
    
    try:
        data = books.find({})
        return  books_entity(data)

    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Error: {e}') from e


@book_router.post('/books/', status_code=status.HTTP_201_CREATED)
async def create_book(bk: Book):
    
    try:

        response = books.insert_one(dict(bk))

        return JSONResponse(content={
            'status_code': status.HTTP_201_CREATED,
            'id': str(response.inserted_id)
        })
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Error: {e}') from e

@book_router.put('/books/{book_id}')
async def update_book(book_id: str, book_updated: Book):
    
    try:

        book = books.find_one({'_id': ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail='The book is not found')

        book_updated.updated_at = datetime.now()
        books.update_one(
            {'_id': ObjectId(book_id)}, 
            {'$set': dict(book_updated)}
        )

        return JSONResponse(content={
            'status_code': status.HTTP_200_OK,
            'Message': "Book updated successfully"
        })

    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Error: {e}') from e

@book_router.delete('/books/{book_id}')
async def delete_book(book_id: str):
    
    book = books.find_one({'_id': ObjectId(book_id)})
    
    if not book:
        raise HTTPException(status_code=404, detail='The book is not found')
    
    response = books.delete_one({'_id': ObjectId(book_id)})
    
    return JSONResponse(content={
            'status_code': status.HTTP_200_OK,
            'Message': "Book deleted successfully"
        })