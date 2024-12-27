from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", ""))
    API_HASH = getenv("API_HASH", "")
    BOT_TOKEN = getenv("BOT_TOKEN", "")
    
    # List of required channels, each with an ID and link
    REQUIRED_CHANNELS = [
        {"id": int(getenv("CHANNEL_1_ID", "")), "link": getenv("CHANNEL_1_LINK", "")},
        {"id": int(getenv("CHANNEL_2_ID", "")), "link": getenv("CHANNEL_2_LINK", "")},
        {"id": int(getenv("CHANNEL_3_ID", "")), "link": getenv("CHANNEL_3_LINK", "")}
        # Add more channels as needed
    ]
    
    SUDO = list(map(int, getenv("SUDO", "").split()))
    MONGO_URI = getenv("MONGO_URI", "")
    
cfg = Config()
