from datetime import datetime

from bson import ObjectId
from models.book import Book
from motor.motor_asyncio import AsyncIOMotorCollection
from schemas.serialize import Serializer
from fastapi import status
from configurations.config import books
from helpers.utils import Response
from configurations.logger import logger


class BookService:
    def __init__(self, book_collection: AsyncIOMotorCollection):
        self.books = book_collection

    async def create(self, book: Book) -> Response:
        """Create a new book document."""
        try:
            serialize_data = Serializer(book)
            response = await self.books.insert_one(serialize_data.serialize())
            if response.acknowledged:
                logger.info(f"Book created successfully: {response.inserted_id}", func_name=self.create.__name__)
                return Response(
                    status_code=status.HTTP_201_CREATED,
                    inserted_id=str(response.inserted_id),
                    message='Book created successfully'
                )
            logger.error("Book not created", func_name=self.create.__name__)
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message='Book not created'
            )
        except Exception as e:
            logger.error(f"Error creating book: {e}", func_name=self.create.__name__)
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f'Error: {e}'
            )

    async def find_all(self) -> Response:
        """Find all books."""
        try:
            data = await self.books.find({}).to_list(None)
            serialize_data = Serializer(data)
            logger.info(f"Fetched {len(data)} books", func_name=self.find_all.__name__)
            return Response(
                status_code=status.HTTP_200_OK,
                data=serialize_data.deserialize()
            )
        except Exception as e:
            logger.error(f"Error fetching books: {e}", func_name=self.find_all.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def find_by_id(self, book_id: str) -> Response:
        """Find a book by its ID."""
        try:
            if book := await self.books.find_one({'_id': ObjectId(book_id)}):
                serialize_data = Serializer(book)
                logger.info(f"Book found: {book_id}", func_name=self.find_by_id.__name__)
                return Response(
                    status_code=status.HTTP_200_OK,
                    data=serialize_data.deserialize()
                )
            logger.warning(f"Book not found: {book_id}", func_name=self.find_by_id.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The book is not found'
            )
        except Exception as e:
            logger.error(f"Error finding book: {e}", func_name=self.find_by_id.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

    async def delete(self, book_id: str) -> Response:
        """Delete a book by its ID."""
        try:
            response = await self.find_by_id(book_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                logger.warning(f"Delete failed, book not found: {book_id}", func_name=self.delete.__name__)
                return response
            delete_result = await self.books.delete_one({'_id': ObjectId(book_id)})
            if delete_result.deleted_count == 1:
                logger.info(f"Book deleted: {book_id}", func_name=self.delete.__name__)
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Book deleted successfully'
                )
            logger.error(f"Book not deleted: {book_id}", func_name=self.delete.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The book is not found'
            )
        except Exception as e:
            logger.error(f"Error deleting book: {e}", func_name=self.delete.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )
    
    async def books_count(self) -> Response:
        """Count all books."""
        try:
            count = await self.books.count_documents({})
            return Response(status_code=status.HTTP_200_OK, data=count)
        except Exception as e:
            return Response(status_code=status.HTTP_404_NOT_FOUND, message=f'Error: {e}')

    async def update(self, book_id: str, book_updated: Book) -> Response:
        """Update a book by its ID."""
        try:
            response = await self.find_by_id(book_id)
            if response.status_code == status.HTTP_404_NOT_FOUND:
                logger.warning(f"Update failed, book not found: {book_id}", func_name=self.update.__name__)
                return response
            book_updated.updated_at = datetime.now()
            update_result = await self.books.update_one({'_id': ObjectId(book_id)}, {'$set': dict(book_updated)})
            if update_result.modified_count == 1:
                logger.info(f"Book updated: {book_id}", func_name=self.update.__name__)
                return Response(
                    status_code=status.HTTP_204_NO_CONTENT,
                    message='Book updated successfully'
                )
            logger.error(f"Book not updated: {book_id}", func_name=self.update.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='The book is not updated'
            )
        except Exception as e:
            logger.error(f"Error updating book: {e}", func_name=self.update.__name__)
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                message=f'Error: {e}'
            )

book_service = BookService(books)