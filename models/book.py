from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
# from uuid import UUID
from datetime import datetime

class Book(BaseModel):
    isbn: str
    title: str
    author: str
    description: Optional[str]
    published: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()