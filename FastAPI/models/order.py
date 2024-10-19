from datetime import datetime
from pydantic import BaseModel, Field

class Order(BaseModel):
    """
    Represents an order of a book.

    Attributes:
    fist_name (str): The first name of the customer.
    last_name (str): The last name of the customer.
    email (str): The email address of the customer.
    book_id (str): The id of the book ordered.
    quantity (int): The number of books ordered.
    created_at (datetime): The timestamp of when the order was created. Defaults to the current time.
    updated_at (datetime): The timestamp of when the order was last updated. Defaults to the current time.
    """
    fist_name: str
    last_name: str
    email: str
    book_id: str
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)