# convert a single book document to a JSON serializable dictionary
def book_entity(book):
    return {
        "_id": (book['_id']),
        "isbn": book['isbn'],
        "title": book['title'],
        "author": book['author'],
        "description": book['description'],
        "published": book['published'],
        "quantity": book['quantity'],
        "created_at": book['created_at'],
        "updated_at": book['updated_at']
    }
    
# convert a list of orders to a JSON serializable list of dictionaries
def books_entity(books):
    return [book_entity(book) for book in books]