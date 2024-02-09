from dotenv import load_dotenv
import os
import discord

load_dotenv()

OBSERVER_TOKEN = os.getenv("OBSERVER_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

ID_LIST = os.getenv("ID_LIST").split(",")

BOT_LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID"))

ADMIN_GUILD_ID = int(os.getenv("ADMIN_GUILD_ID"))
ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID"))
ADMIN_ID = os.getenv("ADMIN_ID")

OBSERVER_HELP_DICT = {
  "observer help": "ヘルプを表示します",
  "observer data <id>": "<id>に該当する人のデータを表示します",
  "observer data-all": "すべての人のデータを表示します",
  "observer chat-ranking": "チャット数ランキングを表示します",
  "observer member": "サーバーのメンバーを表示します",
}