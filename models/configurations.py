import os
import motor.motor_asyncio as motor
from dotenv import load_dotenv
from fastapi import HTTPException

"""
Configure and initialize the MongoDB connection.

This function loads environment variables, sets up the MongoDB connection parameters,
and initializes the client, database, and collection objects.

Returns:
    tuple: A tuple containing the following elements:
        - client (motor.AsyncIOMotorClient): The MongoDB client object.
        - db (motor.AsyncIOMotorDatabase): The database object.
        - books (motor.AsyncIOMotorCollection): The 'Books' collection object.

Raises:
    ValueError: If required environment variables are missing or invalid.
"""
try:
    load_dotenv()

    host = os.environ.get('HOST', str)
    port = int(os.environ.get('PORT'))
    user = os.environ.get('USERNAME', str)
    password = os.environ.get('PASSWORD', str)

    # if not all([host, port, user, password]):
    #     raise HTTPException(status_code=404, detail=f'Error: Missing or invalid environment variables')

    client = motor.AsyncIOMotorClient(f'mongodb://{user}:{password}@{host}:{port}/')

    db = client.library

    books = db.Books
except Exception as e:
    raise HTTPException(status_code=404, detail=f'Error: Missing or invalid environment variables, {e}') from e