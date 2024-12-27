
from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", ""))
    API_HASH = int(getenv("API_HASH", ""))
    BOT_TOKEN = int(getenv("BOT_TOKEN", ""))
    FSUB = int(getenv("FSUB", ""))
    CHID = int(getenv("CHID", ""))
    SUDO = list(map(int, getenv("SUDO", "").split()))
    MONGO_URI = getenv("MONGO_URI", "")
    
cfg = Config()
