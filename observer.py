import discord
from discord.ext import commands
import Config
import database_manager
from cogs import AdminCog, ChatCog, MainCog, WarzoneCog

# 接続に必要なオブジェクトを生成
bot = commands.Bot(
  command_prefix="observer ",
  intents=discord.Intents.all(),
  help_command=None
)

# データベースの作成
database = database_manager.Database(Config.MONGODB_URI, "discord", "user-data")

# Cogの登録
@bot.event
async def setup_hook():
  await bot.add_cog(MainCog(bot))
  await bot.add_cog(AdminCog(bot))
  await bot.add_cog(ChatCog(bot, database))
  await bot.add_cog(WarzoneCog(bot))

def main():
  # Botの起動とDiscordサーバーへの接続
  try:
    bot.run(Config.OBSERVER_TOKEN)
  finally: # サーバーを閉じた時（Ctrl + C）に動く処理
    database.close()
    print("Log out : Observer")

main()