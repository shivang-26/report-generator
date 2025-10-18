from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = None
db = None

async def connect_to_mongo():
    global client, db
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.get_database("report_generator")
        # Test the connection
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        return db
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    if client:
        client.close()

# Collections
def get_reports_collection():
    return db.reports

def get_users_collection():
    return db.users
