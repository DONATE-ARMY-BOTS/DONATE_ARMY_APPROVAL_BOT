
from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", ""))
    API_HASH = getenv("API_HASH", "")
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    FSUB = getenv("FSUB", "DONATE_ARMY_BOTS")
    CHID = int(getenv("CHID", "-1002329214096"))
    SUDO = list(map(int, getenv("SUDO", "5347809540").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://DONATE_ARMY:bgmi_009@cluster0.erxioab.mongodb.net/?retryWrites=true&w=majority")
    
cfg = Config()
