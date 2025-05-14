from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
# from uuid import UUID
from datetime import datetime

class Book(BaseModel):
    """
    A class representing a book with attributes such as ISBN, title, author, description, 
    publication year, and timestamps for creation and last update.

    Attributes:
    isbn (str): The International Standard Book Number of the book.
    title (str): The title of the book.
    author (str): The author of the book.
    description (Optional[str]): A brief description of the book.
    published (int): The year the book was published.
    created_at (datetime): The timestamp of when the book was created. Defaults to the current time.
    updated_at (datetime): The timestamp of when the book was last updated. Defaults to the current time.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    isbn: str
    title: str
    author: str
    description: Optional[str]
    published: int
    quantity: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)