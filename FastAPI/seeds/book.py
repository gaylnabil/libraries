from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.book import Book
from configurations.config import books
from motor.motor_asyncio import AsyncIOMotorCollection
from configurations.logger import logger

seed_router = APIRouter()

def write_csv(filename: str, list_books: list[Book]):
    if len(list_books) != 0:
        with open(filename, 'a') as f:
            for book in list_books:
                f.write(f"{str(book['_id'])},{book['title']},{book['author']},{book['description']},"
                        f"{book['published']},{book['quantity']},{book['created_at']},{book['updated_at']}\n")

async def read_csv(filename: str, books: AsyncIOMotorCollection):
    count = await books.count_documents({})
    print("Count:", count)
    if count == 0:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    _id, title, author, description, published, quantity, created_at, updated_at = line.split(',')
                    await books.insert_one({
                        '_id': ObjectId(_id),
                        'title': title,
                        'author': author,
                        'description': description,
                        'published': published,
                        'quantity': quantity,
                        'created_at': created_at,
                        'updated_at': updated_at
                    })
@seed_router.get("/books/seeds/write_to")
async def write_books():
    try:
        data = await books.find({}).to_list(None)
        write_csv('books.csv', data)
    except Exception as e:
        logger.error(f"Error: {e}", stacklevel=2)
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

    logger.info("Books are written in csv file successfully", stacklevel=2)

    return JSONResponse(content={
            'status_code': status.HTTP_201_CREATED,
            'Message': "Books are written in csv file successfully"
    })

@seed_router.post("/books/seeds/read_from")
async def read_books():
    try:
        await read_csv('books.csv',  books)
        logger.info("Books are read from csv file successfully", stacklevel=2)
    except Exception as e:
        logger.error(f"Error: {e}", stacklevel=2)
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

    return JSONResponse(content={
            'status_code': status.HTTP_201_CREATED,
            'Message': "Books are read from csv file successfully"
    })