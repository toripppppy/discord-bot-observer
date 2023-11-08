from dotenv import load_dotenv
import os
import discord

load_dotenv()

OBSERVER_TOKEN = os.getenv("OBSERVER_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

ID_LIST = os.getenv("ID_LIST").split(",")

CHANNEL_ID = dict()
for text in os.getenv("CHANNEL_ID").split(","):
  key, value = text.split(":")
  value = int(value)
  CHANNEL_ID[key] = value

ADMIN_GUILD_ID = int(os.getenv("ADMIN_GUILD_ID"))
ADMIN_ID = os.getenv("ADMIN_ID")

OBSERVER_HELP_DICT = {
  "observer help": "ヘルプを表示します",
  "observer data <id>": "<id>に該当する人のデータを表示します",
  "observer data-all": "すべての人のデータを表示します",
  "observer chat-ranking": "チャット数ランキングを表示します",
  "observer member": "サーバーのメンバーを表示します",
}

EMBED_COLOR_WHITE = 0xF0F0FF
EMBED_COLOR_YELLOW = 0xFFFF00
EMBED_COLOR_RED = 0xFF0000
EMBED_COLOR_GREEN = 0x00FF00
BASE_EMBED = discord.Embed(title = "Observer", color = EMBED_COLOR_WHITE)