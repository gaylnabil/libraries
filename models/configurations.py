import os
import motor.motor_asyncio as motor
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

host = os.environ.get('HOST', str)
port = int(os.environ.get('PORT'))
user = os.environ.get('USERNAME', str)
password = os.environ.get('PASSWORD', str)

# client = MongoClient(
#             host, 
#             port, 
#             username=user, 
#             password=password
#         )

client = motor.AsyncIOMotorClient(f'mongodb://{user}:{password}@{host}:{port}/')

db = client.library

books = db.Books