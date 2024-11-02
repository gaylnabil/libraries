from datetime import datetime

from bson import ObjectId
from models.book import Book
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.serialize import Serializer
from fastapi import status
from configurations.config import books
from helpers.utils import Response


class BookService:
    def __init__(self, book_collection: AsyncIOMotorCollection):
        self.books = book_collection

    async def create(self, book: Book) -> Response:
        try:
            serialize_data = Serializer(book)
            response = await self.books.insert_one(serialize_data.serialize())
            if response.acknowledged:
                return Response(
                    status_code=status.HTTP_201_CREATED,
                    inserted_id=str(response.inserted_id),
                    message='Book created successfully'

                )

            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message='Book not created'
            )

        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f'Error: {e}'
            )

    async def find_all(self) -> Response:
        try:
            data = await self.books.find({}).to_list(None)
            serialize_data = Serializer(data)
            return Response(
                status_code=status.HTTP_200_OK,
                data=serialize_data.deserialize()
            )
        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def find_by_id(self, book_id: str) -> Response:
        try:
            if book := await self.books.find_one({'_id': ObjectId(book_id)}):
                serialize_data = Serializer(book)
                return Response(
                    status_code=status.HTTP_200_OK,
                    data=serialize_data.deserialize()
                )

            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The book is not found'
            )
        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def delete(self, book_id: str) -> Response:
        try:

            response = await self.find_by_id(book_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return response

            if await self.books.delete_one({'_id': ObjectId(book_id)}):
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Book deleted successfully'
                )

            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The book is not found'
            )

        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def update(self, book_id: str, book_updated: Book) -> Response:
        try:
            response = await self.find_by_id(book_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return response
            book_updated.updated_at = datetime.now()
            response = await self.books.update_one({'_id': ObjectId(book_id)}, {'$set': dict(book_updated)})
            print("response: ", response)
            if response.acknowledged:
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Book updated successfully'
                )

            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The book is not updated'
            )

        except Exception as e:
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

book_service = BookService(books)