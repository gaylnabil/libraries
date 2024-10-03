
def book_entity(book):
    return {
        "id": str(book['_id']),
        "isbn": book['isbn'],
        "title": book['title'],
        "author": book['author'],
        "description": book['description'],
        "published": book['published'],
        "created_at": book['created_at'],
        "updated_at": book['updated_at']
    }
    
def books_entity(books):
    return [book_entity(book) for book in books]

