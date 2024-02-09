import discord
from discord.ext import commands
import Config
import database_manager
from others import Embed, Utils

# 接続に必要なオブジェクトを生成
bot = commands.Bot(
  command_prefix="observer ",
  intents=discord.Intents.all(),
  help_command=None
)

# データベースの作成
database = database_manager.Database(Config.MONGODB_URI, "discord", "user-data")

# ヘルプ
@bot.command(name="help")
async def help(message):
  print("help")
  embed = Embed.make_embed()
  for command, description in Config.OBSERVER_HELP_DICT.items():
    embed.add_field(name = command, value = description, inline = False)
  await message.channel.send(embed = embed)

# 指定のユーザーデータを表示
@bot.command(name="data")
async def data(message, author):
  data = database.return_data(author)
  if data:
    text = Utils.create_data_text(data)
    embed = Embed.make_embed(description=text)
  else:
    embed = Embed.make_embed("red", f"「{author}」のデータは見つかりませんでした。")
  await message.channel.send(embed = embed)

# ユーザーデータを全て表示
@bot.command(name="data-all")
async def data_all(message):
  for member in message.guild.members:
    # Botだった場合
    if member.bot: continue
    # data関数を呼び出す
    await data(message, member.name)

# チャットランキングを表示
@bot.command(name="chat-ranking")
async def chat_ranking(message):
  chat_data = database.return_chat_ranking()
  text = Utils.create_chat_ranking_text(chat_data)
  embed = Embed.make_embed(description=text)
  await message.channel.send(embed = embed)

# メンバー一覧を表示
@bot.command(name="member")
async def member(message):
  text = Utils.create_member_list_text(message)
  embed = Embed.make_embed(description=text)
  await message.channel.send(embed = embed)

# アドミンコマンドのルーティング
@bot.command(name="admin")
async def admin_router(ctx, arg = None):
  # 引数の指定がない場合は無視
  # TODO embedを出すべき
  if arg is None: return

  # 管理者以外には発動できない
  if str(ctx.author.id) != Config.ADMIN_ID:
    print("you are not admin")
    return
  # adminチャンネル以外では発動できない
  if not ctx.channel.id == Config.ADMIN_CHANNEL_ID:
    print("please try again in admin channel")
    return
  
  if arg == "logout":
    # ログアウト処理
    embed = Embed.make_embed("yellow", "終了します。")
    channel = bot.get_channel(Config.BOT_LOG_CHANNEL_ID)
    await channel.send(embed = embed)
    await bot.close()

# 起動時に動作する処理
@bot.event
async def on_ready():
  print('Log in : Observer', flush = True)
  embed = Embed.make_embed("yellow", "起動しました。")
  channel = bot.get_channel(Config.BOT_LOG_CHANNEL_ID)
  await channel.send(embed = embed)

# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
  author = message.author
  content = message.content
  
  # メッセージが空（写真）の場合
  if not content: return
  
  # Botだった場合
  if author.bot: return
  
  # メッセージ送信をした際のデータベース処理
  database.chat(author.name, content)
  level = database.return_level(author.name)
  chat = database.return_chat(author.name)
  length = database.return_length(author.name)
  level_up_cnt = Utils.return_level_up_cnt(level, chat, length)
  if level_up_cnt > 0: # レベルアップした場合
    database.update_level(author.name, level_up_cnt)
    embed = Embed.make_embed("green", f"{author.name}がレベルアップしました！（Lv:{level} → Lv:{level+level_up_cnt}）")
    await message.channel.send(embed = embed)
  database.log()

  # コマンドを実行 存在しなければエラー
  ctx = await bot.get_context(message)
  if ctx.command is None:
    embed = Embed.make_embed("red", description="無効なコマンドです。\n`observer help`でヘルプを表示できます。")
    await message.channel.send(embed = embed)
  else:
    await bot.process_commands(message)

def main():
  # Botの起動とDiscordサーバーへの接続
  try:
    bot.run(Config.OBSERVER_TOKEN)
  finally: # サーバーを閉じた時（Ctrl + C）に動く処理
    database.close()
    print("Log out : Observer")

main()