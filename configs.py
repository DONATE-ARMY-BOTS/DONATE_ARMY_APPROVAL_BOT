from dotenv import load_dotenv
from os import getenv

# Load environment variables from .env file
load_dotenv()

class Config:
    API_ID = getenv("API_ID", "")
    API_HASH = getenv("API_HASH", "")
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    SUDO = list(map(int, getenv("SUDO", "").split()))
    MONGO_URI = getenv("MONGO_URI", "")
    REQUIRED_CHANNELS = getenv("REQUIRED_CHANNELS", "").split()  # Multiple channels

cfg = Config()
