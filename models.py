from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Any, List, Optional
from uuid import UUID
class Book(BaseModel):
    
    id: str | None = None
    isbn: str = Field()
    title: str = Field()
    author: str = Field()
    description: Optional[str] = Field()
    publish: int = Field()
