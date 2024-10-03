import os

from pymongo import MongoClient

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