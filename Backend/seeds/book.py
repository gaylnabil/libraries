from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.book import Book
from configurations.config import books
from configurations.logger import logger
from services.book import book_service
seed_router = APIRouter()

def write_to_csv(filename: str, list_books: list[Book]):
    """Write books to csv file."""
    
    if len(list_books) == 0:
        return
    
    with open(filename, 'a') as f:
        for book in list_books:
            f.write(f"{str(book['_id'])},{book['title']},{book['author']},{book['description']},"
                    f"{book['published']},{book['quantity']},{book['created_at']},{book['updated_at']}\n")

async def read_from_csv(filename: str):
    """Read books from csv file."""
    
    result = await book_service.books_count()
    print("Count:", result.data)
    
    if result.data > 0:
        return
    
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
                    
@seed_router.get("/books/seeds/write_to_csv")
async def write_books_to_csv():
    try:
        result = await book_service.find_all()
        write_to_csv('books.csv', result.data)
    except Exception as e:
        logger.error(f"Error: {e}", stack_level=2)
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

    logger.info("Books are written in csv file successfully", stack_level=2)

    return JSONResponse(content={
            'status_code': status.HTTP_201_CREATED,
            'Message': "Books are written in csv file successfully"
    })

@seed_router.post("/books/seeds/read_from_csv")
async def read_books_from_csv():
    try:
        await read_from_csv('books.csv')
        logger.info("Books are read from csv file successfully", stack_level=2)
    except Exception as e:
        logger.error(f"Error: {e}", stack_level=2)
        raise HTTPException(status_code=404, detail=f"Error: {e}") from e

    return JSONResponse(content={
            'status_code': status.HTTP_201_CREATED,
            'Message': "Books are read from csv file successfully"
    })