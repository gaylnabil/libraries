from fastapi import FastAPI, HTTPException
from typing import List
from models import Book
from uuid import UUID, uuid4
app = FastAPI()

books = []
@app.get('/')
async def root():
    return {'message': 'Hello World'}

