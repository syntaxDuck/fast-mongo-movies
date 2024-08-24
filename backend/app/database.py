from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote, urlencode

class MongoDBConfig:
    def __init__(self, username: str, password: str, host: str, **kwargs) -> None:
        self.username: str = username
        self.password: str = password
        self.host: str = host
        self.options: kwargs = kwargs

    def build_mongo_atlas_uri(self) -> str:
        # URL-encode the username and password
        encoded_username = quote(self.username)
        encoded_password = quote(self.password)
        
        base_uri = f"mongodb+srv://{encoded_username}:{encoded_password}@{self.host}/"
        
        # if self.dbname:
        #     base_uri += f"/{self.dbname}"
        
        if self.options:
            query_params = urlencode(self.options)
            base_uri += '?' + query_params
        
        return base_uri
    
class MongoDBConnection:
    def __init__(self, config: MongoDBConfig) -> None:
        self._config = config
        self._client: AsyncIOMotorClient = None

    @property
    async def client(self):
        if self._client is None and self._config:
            await self.get_db_connection()
        return self._client
    
    @client.setter
    def client(self, config: MongoDBConfig):
        self._config = config
        self.get_db_connection()

    async def get_db_connection(self) -> None:
        uri = self._config.build_mongo_atlas_uri()
        client = AsyncIOMotorClient(uri)

        try:
            await self.ping_server(client)
            self._client = client
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")

    async def ping_server(self, client) -> None:
        try:
            await client.admin.command("ping")
            print("Ping successful...")
        except Exception as e:
            print(f"Ping failed: {e}")
       
           
           
