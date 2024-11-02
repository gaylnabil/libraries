import json
from contextlib import asynccontextmanager
from datetime import datetime
from logging.config import fileConfig

from bson import ObjectId, json_util
from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.book import Book
from configurations.config import books
from schemas.book_schema import book_entity, books_entity

from configurations.logger import logger

from schemas.serialize import Serializer


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
# This router handle all the CRUD operations for books
# including retrieving, creating, updating and deleting
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Nabil Book CSV : Enter")
    # await read_csv('books.csv')
    yield
    print("Gayl Book : Exit")
    await shutdown()

book_router = APIRouter(lifespan=lifespan)
# book_router.lifespan_context = lifespan

async def shutdown():
    print("Shutting down...")

@book_router.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def retrieve_book(book_id: str):

    try:
        if book := await books.find_one(ObjectId(book_id)):

            serialize_data = Serializer(book)
            book = serialize_data.deserialize()
            logger.info('Retrieved the book: %s', book, func_name=retrieve_book.__name__)

            return book

        else:
            logger.error('The book is not found', func_name=retrieve_book.__name__)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The book is not found')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

@book_router.get("/books/", status_code=status.HTTP_200_OK)
async def get_books():

    try:
        data = await books.find({}).to_list(None)
        logger.info("find all books successfully", func_name=get_books.__name__)
        serialize_data = Serializer(data)
        return serialize_data.deserialize()

    except Exception as e:
        logger.error(f"Error: {e}", stacklevel=2)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e


@book_router.post('/books/', response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(bk: Book):

    try:
        serialize_data = Serializer(bk)
        response = await books.insert_one(serialize_data.serialize())

        if response.acknowledged:
            logger.info("Book created successfully, status code: %s, Id: %s", status.HTTP_201_CREATED, response.inserted_id, func_name=create_book.__name__)
            return JSONResponse(content={
                'status_code': status.HTTP_201_CREATED,
                'id': str(response.inserted_id)
            })

        logger.error("Book not created", func_name=create_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not created')

    except Exception as e:
        logger.error(f"Error: {e}", func_name=create_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

@book_router.put('/books/{book_id}', response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: str, book_updated: Book):

    try:

        book = await books.find_one({'_id': ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The book is not found')

        book_updated.updated_at = datetime.now()

        serialize_data = Serializer(book_updated)
        response = await books.update_one(
            {'_id': ObjectId(book_id)},
            {'$set': serialize_data.serialize()}
        )

        if response.acknowledged:
            logger.info("Book updated successfully, status code: %s, Id: %s", status.HTTP_200_OK, book_id, func_name=update_book.__name__)
            return JSONResponse(content={
                'status_code': status.HTTP_200_OK,
                'id': str(response.inserted_id)
            })

        logger.error("Book not updated", func_name=update_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not updated')

    except Exception as e:
        logger.error(f"Error: {e}", func_name=update_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e

@book_router.delete('/books/{book_id}')
async def delete_book(book_id: str):

    try:
        book = await books.find_one({'_id': ObjectId(book_id)})
        if not book:
            logger.error(f"The book is not found, %s", status.HTTP_400_BAD_REQUEST, func_name=delete_book.__name__)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The book is not found')

        await books.delete_one({'_id': ObjectId(book_id)})

        logger.info("Book deleted successfully, status code: %s, Id: %s", status.HTTP_200_OK, book_id, func_name=delete_book.__name__)
        return JSONResponse(content={
            'status_code': status.HTTP_200_OK,
            'Message': "Book deleted successfully"
        })

    except Exception as e:
        logger.error(f"Error: {e}", func_name=delete_book.__name__)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: {e}') from e