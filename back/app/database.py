from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncIterator

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.local  # 'local' 데이터베이스 사용

def get_db():
    return database