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
        - orders (motor.AsyncIOMotorCollection): The 'Books' collection object.

Raises:
    ValueError: If required environment variables are missing or invalid.
"""
try:
    load_dotenv()

    host = os.environ.get('MONGO_HOST', str)
    port = os.environ.get('MONGO_PORT', int)
    user = os.environ.get('MONGO_USERNAME', str)
    password = os.environ.get('MONGO_PASSWORD', str)

    # if not all([host, port, user, password]):
    #     raise HTTPException(status_code=404, detail=f'Error: Missing or invalid environment variables')

    client = motor.AsyncIOMotorClient(f'mongodb://{user}:{password}@{host}:{port}/')

    db = client.library
    books = db.Books
    orders = db.Orders

except Exception as e:
    raise HTTPException(status_code=404, detail=f'Error: Missing or invalid environment variables, {e}') from e