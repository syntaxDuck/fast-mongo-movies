from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor
from urllib.parse import quote, urlencode

class MongoDBConfig:
    """
    A MongoDB configuration object.

    Attributes:
        username (str): The username for the MongoDB connection.
        password (str): The password for the MongoDB connection.
        host (str): The host for the MongoDB connection.
        options (dict): Additional keyword arguments for the MongoDB connection.
    """

    def __init__(self, username: str, password: str, host: str, **kwargs) -> None:
        self._username = username
        self._password = password
        self._host = host
        self._options = kwargs

    def build_mongo_atlas_uri(self) -> str:
        """
        Builds a MongoDB Atlas URI based on the provided configuration.

        Returns:
            str: The MongoDB Atlas URI.
        """
        # URL-encode the username and password
        encoded_username = quote(self._username)
        encoded_password = quote(self._password)
        
        base_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{self._host}/"
        
        # if self.dbname:
        #     base_uri += f"/{self.dbname}"
        
        if self._options:
            query_params = urlencode(self._options)
            base_uri += '?' + query_params
        
        return base_uri
    
class MongoDBConnection:
    def __init__(self, config: MongoDBConfig) -> None:
        """
        Initializes a MongoDB connection object.

        Args:
            config (MongoDBConfig): The MongoDB configuration object.
        """
        self._config = config
        self._client: AsyncIOMotorClient = None
        self._databases: list[str] = []

    @property
    async def client(self) -> AsyncIOMotorClient:
        """
        A property that asynchronously establishes a connection to a MongoDB server.
        
        Returns:
            AsyncIOMotorClient: The established MongoDB client connection.
        """
        if self._client is None:
            await self._initialize_client()
        return self._client

    @client.setter
    def client(self, config: MongoDBConfig) -> None:
        """
        Sets the client configuration and resets the connection.

        Args:
            config (MongoDBConfig): The MongoDB configuration object.
        """
        self._config = config
        self._client = None

    @property
    async def databases(self) -> list[str]:
        """
        A property that returns a list of all databases in the MongoDB server.

        Returns:
            list: A list of all database names in the server.
        """
        if not self._databases:
            await self._initialize_client()
            self._databases = await self.list_databases()
        return self._databases

    async def _initialize_client(self) -> None:
        if self._client is None:
            await self._get_db_connection()

    async def _get_db_connection(self) -> None:
        """
        Asynchronously establishes a connection to a MongoDB server.
        """
        uri = self._config.build_mongo_atlas_uri()
        self._client = AsyncIOMotorClient(uri)
        
        try:
            await self.ping_server()
        except PyMongoError as e:
            print(f"Failed to connect to MongoDB: {e}")
            self._client = None

    async def ping_server(self) -> None:
        """
        Asynchronously pings a MongoDB server to confirm a successful connection.
        """
        if self._client is None:
            await self._initialize_client()

        try:
            await self._client.admin.command("ping")
            print("Ping successful...")
        except PyMongoError as e:
            print(f"Ping failed: {e}")

    async def list_databases(self) -> list[str]:
        """
        Asynchronously lists all databases in the MongoDB server.
        
        Returns:
            list: A list of database names.
        """
        if self._client is None:
            await self._initialize_client()

        try:
            return await self._client.list_database_names()
        except PyMongoError as e:
            print(f"Error listing databases: {e}")
            return []

    async def fetch_documents(self, database_name: str, collection_name: str, filter_query: dict = None) -> list[dict]:
        """
        Asynchronously queries the specified collection and returns the documents.

        Args:
            database_name (str): The database name.
            collection_name (str): The collection name.
            filter_query (dict, optional): The query filter.

        Returns:
            list: A list of documents matching the filter.
        """
        if self._client is None:
            await self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][collection_name]
            cursor: AsyncIOMotorCursor = collection.find(filter_query)
            return await cursor.to_list(length=None)
        except PyMongoError as e:
            print(f"Error fetching documents: {e}")
            return []
        
    async def insert_documents(self, database_name: str, collection_name: str, documents: list[dict]) -> None:
        if self._client is None:
            await self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][collection_name]
            restult = await collection.insert_many(documents)
        except PyMongoError as e:
            print(f"Error inserting documents: {e}")
        finally:
            return restult.inserted_ids

    async def update_documents(self, database_name: str, collection_name: str, filter_query: dict, update_query: dict) -> None:
        if self._client is None:
            await self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][collection_name]
            result = await collection.update_many(filter_query, update_query)
        except PyMongoError as e:
            print(f"Error updating document: {e}")
        finally:
            result = result.modified_count
    async def delete_documents(self, database_name: str, collection_name: str, filter_query: dict) -> None:
        if self._clinet is None:
            self._initialize_client()

        try:
            collection: AsyncIOMotorCollection = self._client[database_name][collection_name]
            result = await collection.delete_many(filter_query)
        except PyMongoError as e:
            print(f"Error deleting document: {e}")
        finally:
            result = result.deleted_count
    async def __aenter__(self):
        await self._initialize_client()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._client:
            self._client.close()
    
    def __del__(self):
        if self._client:
            self._client.close()
