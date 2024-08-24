from dotenv import load_dotenv
from types import SimpleNamespace
import os

load_dotenv()

settings = SimpleNamespace()
settings.HOST = os.getenv("DB_HOST")
settings.USER = os.getenv("DB_USER")
settings.PASS = os.getenv("DB_PASS")

