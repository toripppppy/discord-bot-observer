from dotenv import load_dotenv
import os

load_dotenv()

OBSERVER_TOKEN = os.getenv("OBSERVER_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

ID_LIST = os.getenv("ID_LIST").split(",")

BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID"))

ADMIN_GUILD_ID = int(os.getenv("ADMIN_GUILD_ID"))
ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID"))
ADMIN_ID = os.getenv("ADMIN_ID")