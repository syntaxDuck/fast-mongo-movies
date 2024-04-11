import asyncio
from config import settings
from urllib.parse import quote
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


async def get_db_connection():
    # Replace the placeholder with your Atlas connection string
    uri = settings.PROTOCOL + settings.DB_USER + ":" + settings.PASS + settings.HOST

    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))

    try:
        await ping_server(client)
        return client
    except Exception as e:
        print(e)


async def ping_server(client):

    # Send a ping to confirm a successful connection
    try:
        await client.admin.command("ping")
        print("Ping successful...")
    except Exception as e:
        print(e)
