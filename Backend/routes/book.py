import json
from contextlib import asynccontextmanager
from datetime import datetime
from bson import ObjectId
from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.book import Book
from configurations.logger import logger
from services.book import book_service

# This router handle all the CRUD operations for orders
# including retrieving, creating, updating and deleting
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Nabil Book CSV : Enter")
    # await read_csv('orders.csv')
    yield
    print("Gayl Book : Exit")
    await shutdown()

book_router = APIRouter(lifespan=lifespan)
# book_router.lifespan_context = lifespan

async def shutdown():
    print("Shutting down...")

# RETRIEVE /orders/{book_id}
@book_router.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def retrieve_book_by_id(book_id: str) -> JSONResponse:

    try:
        response = await book_service.find_by_id(book_id)
        if response.status_code == status.HTTP_200_OK:
            logger.info('Retrieved the book: %s', response.data, func_name=retrieve_book_by_id.__name__)
            return response.data

        logger.error('The book is not found', func_name=retrieve_book_by_id.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The book is not found')

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

# GET /orders
@book_router.get("/books/", status_code=status.HTTP_200_OK)
async def get_books() -> JSONResponse:
    try:
        response = await book_service.find_all()
        if response.status_code == status.HTTP_200_OK:
            logger.info("Retrieved all orders successfully", func_name=get_books.__name__)
            return response.data

        logger.error("The orders are not found", func_name=get_books.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The orders are not found')
    except Exception as e:
        logger.error(f"Error: {e}", func_name=get_books.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

# POST /orders
@book_router.post('/books/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(bk: Book):

    try:
        response = await book_service.create(bk)
        if response.status_code == status.HTTP_201_CREATED:
            logger.info("Book created successfully, status code: %s, Id: %s", status.HTTP_201_CREATED, response.inserted_id, func_name=create_book.__name__)
            return JSONResponse(content={
                'status_code': status.HTTP_201_CREATED,
                'message':  response.message,
                'inserted_id': response.inserted_id
            })

        logger.error("Book not created", func_name=create_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not created')

    except Exception as e:
        logger.error(f"Error: {e}", func_name=create_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

# PUT /orders/{book_id}
@book_router.put('/books/{book_id}', response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: str, book_updated: Book) -> JSONResponse:

    try:
        response = await book_service.update(book_id, book_updated)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            logger.info("Book updated successfully, status code: %s, Id: %s", status.HTTP_204_NO_CONTENT, book_id, func_name=update_book.__name__)
            return JSONResponse(content={
                'status_code': status.HTTP_204_NO_CONTENT,
                'message':  response.message,
            })

        logger.error("Book not updated", func_name=update_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not updated')

    except Exception as e:
        logger.error(f"Error: {e}", func_name=update_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

# DELETE /orders/{book_id}
@book_router.delete('/books/{book_id}')
async def delete_book(book_id: str) -> JSONResponse:

    try:
        response = await book_service.find_by_id(book_id)

        if response.status_code != status.http.HTTP_204_NO_CONTENT:
            logger.error(f"The book is not found, %s", status.HTTP_400_BAD_REQUEST, func_name=delete_book.__name__)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The book is not found')

        response = await book_service.delete({'_id': ObjectId(book_id)})

        if response.status_code == status.HTTP_200_OK:
            logger.info("Book deleted successfully, status code: %s, Id: %s", status.HTTP_200_OK, book_id, func_name=delete_book.__name__)
            return JSONResponse(content={
                'status_code': status.HTTP_200_OK,
                'message': response.message,
            })

        logger.error("Book not deleted", func_name=delete_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not deleted')

    except Exception as e:
        logger.error(f"Error: {e}", func_name=delete_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e