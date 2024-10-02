from typing import Optional
from pydantic import BaseModel
from typing import Any, List, Optional
from uuid import UUID
class Book(BaseModel):
    
    id: Optional[UUID] = None
    isbn: str
    title: str
    author: str
    description: Optional[str]
    publish: int
