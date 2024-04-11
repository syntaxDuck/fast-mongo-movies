import asyncio
from database import get_db_connection
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


async def ping_server():
    # Replace the placeholder with your Atlas connection string
    uri = "mongodb+srv://kamcomer96code:test@cluster0.hbc7yul.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


asyncio.run(ping_server())
