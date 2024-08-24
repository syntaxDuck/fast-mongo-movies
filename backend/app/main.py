import asyncio
from config import settings
from database import MongoDBConfig, MongoDBConnection
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
)


async def query_server(db):
    # Send a ping to confirm a successful connection
    try:
        # await client.admin.command("ping")
        if db is None:
            return None

        print("Pinged your deployment. You successfully connected to MongoDB!")
        collection: AsyncIOMotorCollection = db.myDatabase.recipes
        cursor: AsyncIOMotorCursor = collection.find()

        # Convert cursor to list
        documents = await cursor.to_list(length=None)

        # Print the documents
        for document in documents:
            print(document)
    except Exception as e:
        print(e)

async def main():
    # Assuming settings is already defined with USER, PASS, and HOST
    config = MongoDBConfig(settings.USER, settings.PASS, settings.HOST, appName='Cluster0', tls='true', tlsAllowInvalidCertificates='true', retryWrites='true', w='majority')
    mongo_connection = MongoDBConnection(config)
    
    # Await the client property to establish the connection and ping the server
    client = await mongo_connection.client
    
    # Optionally, directly call the ping_server method to confirm connection
    await query_server(client)

if __name__ == '__main__':
    asyncio.run(main())