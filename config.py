import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if it exists)
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devsecret")
    DATABASE_URL = str(os.environ.get("DATABASE_URL", "sqlite:///my_holiday.db"))
    SESSION_TYPE = "filesystem"

# Optional: Print the loaded value (for debugging only; remove in production)
print("DATABASE_URL loaded as:", os.environ.get("DATABASE_URL"))
