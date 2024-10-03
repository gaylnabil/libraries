import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

host = os.environ.get('HOST', str)
port = int(os.environ.get('PORT'))
user = os.environ.get('USERNAME', str)
password = os.environ.get('PASSWORD', str)

client = MongoClient(
            host, 
            port, 
            username=user, 
            password=password
        )
# client = MongoClient('mongodb://root:password@db:27017/')
db = client.library

books = db.Books