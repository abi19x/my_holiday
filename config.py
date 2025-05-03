import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devsecret")
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://myuser:masteRh0512.@localhost:5433/mydb")
    SESSION_TYPE = "filesystem"
