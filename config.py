import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "cricbuzz"),
    "port": int(os.getenv("DB_PORT", 3307)),
}

API_CONFIG = {
    "key": os.getenv("RAPIDAPI_KEY"),
    "host": os.getenv("RAPIDAPI_HOST"),
    "base_url": "https://cricbuzz-cricket.p.rapidapi.com"
}