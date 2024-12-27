
from os import path, getenv

class Config:
    API_ID = getenv("API_ID", "")
    API_HASH = getenv("API_HASH", "")
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    FSUB = getenv("FSUB", "")
    CHID = getenv("CHID", "")
    SUDO = list(map(int, getenv("SUDO", "").split()))
    MONGO_URI = getenv("MONGO_URI", "")
    
cfg = Config()
