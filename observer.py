import discord
import Config
import database_manager
import others.Utils as Utils
import others.Embed as Embed
from others import Data

# 接続に必要なオブジェクトを生成
discord_client = discord.Client(intents=discord.Intents.all())

# データベースの作成
database = database_manager.Database(Config.MONGODB_URI, "discord", "user-data")

# コマンドの関数
async def help(message):
  print("help")
  embed = Embed.make_embed()
  for command, description in Config.OBSERVER_HELP_DICT.items():
    embed.add_field(name = command, value = description, inline = False)
  await message.channel.send(embed = embed)

async def data(message, author):
  data = database.return_data(author)
  if data:
    text = Utils.create_data_text(data)
    embed = Embed.make_embed(description=text)
  else:
    embed = Embed.make_embed("red", f"「{author}」のデータは見つかりませんでした。")
  await message.channel.send(embed = embed)

async def data_all(message):
  for member in message.guild.members:
    # Botだった場合
    if member.bot: continue
    # data関数を呼び出す
    await data(message, member.name)

async def chat_ranking(message):
  chat_data = database.return_chat_ranking()
  chat_data = sorted(chat_data.items(), key=lambda x:x[1], reverse=True)
  text = "===== チャット数ランキング =====\n"
  for i, (name, chat) in enumerate(chat_data):
    text += f"　第{i+1}位：{name}（{chat}回）\n"
  text += "=" * (20 + 1 + len("チャット数ランキング"))
  embed = Embed.make_embed(description=text)
  await message.channel.send(embed = embed)

async def member(message):
  max_string_length = 0 # 動的に[=]の文字数を変更するための変数
  text = ""             # for文で作成するテキスト
  output_text = ""      # 最終的に送信するテキスト
  
  for member in message.guild.members:
    # Botだった場合
    if member.bot: continue
    
    text += "・"
    string_length = 2 # 最初に[・]の文字数分を足す
    
    # ニックネームがなかった場合
    if member.nick == None:
      text += member.name
      string_length += Utils.check_width(member.name)
    else:
      text += member.name + "「" + member.nick + "」"
      string_length += Utils.check_width(member.name + "「" + str(member.nick) + "」")
    
    # Role があったら記述する
    role_list = [role.name for role in member.roles if role.name != "@everyone"]
    role_text = ""
    if len(role_list) != 0:
      role_text += "［"
      role_text += "  ".join(role_list)
      role_text += "］\n"
    else:
      role_text += "\n"
    
    text += role_text
    string_length += Utils.check_width(role_text)
    
    # 最大文字数を更新
    max_string_length = max(max_string_length, string_length)

  # 最大文字数が奇数だった場合偶数にする
  # これをしないと[=]の文字数が合わなくなる
  if max_string_length % 2:
    max_string_length += 1
  
  # [=]の文字数を計算
  # -14 は " メンバー一覧 " の文字数
  # // 2 は両端に [=] を付けるため
  x = (max_string_length - 13) // 2
  output_text += ("=" * x) + " メンバー一覧 " + ("=" * x) + "\n"
  output_text += text
  output_text += "=" * (max_string_length - 1)
  
  embed = Embed.make_embed(description=output_text)
  await message.channel.send(embed = embed)

# コマンドのルーティング
async def router(message, command):
  if command[1] == "help":
    await help(message)
  elif command[1] == "data" and len(command) == 3:
    await data(message, command[2])
  elif command[1] == "data-all":
    await data_all(message)
  elif command[1] == "chat-ranking":
    await chat_ranking(message)
  elif command[1] == "member":
    await member(message)
  else:
    embed = Embed.make_embed("red", description="無効なコマンドです。\n`observer help`でヘルプを表示できます。")
    await message.channel.send(embed = embed)

# アドミンコマンドのルーティング
async def admin_router(message, command):
  if command[1] == "logout":
    embed = Embed.make_embed("yellow", "終了します。")
    channel = discord_client.get_channel(Config.BOT_LOG_CHANNEL_ID)
    await channel.send(embed = embed)
    await discord_client.close()

# 起動時に動作する処理
@discord_client.event
async def on_ready():
  print('Log in : Observer', flush = True)
  embed = Embed.make_embed("yellow", "起動しました。")
  channel = discord_client.get_channel(Config.BOT_LOG_CHANNEL_ID)
  await channel.send(embed = embed)

# メッセージ受信時に動作する処理
@discord_client.event
async def on_message(message):
  author = message.author
  content = message.content
  
  # メッセージが空（写真）の場合
  if not content: return
  
  content_split = list(map(str.lower ,content.split()))
  
  # Botだった場合
  if author.bot: return
  
  # アドミンコマンドかの判定 & アドミンコマンドの実行
  if content_split[0] == "admin" and len(content_split) >= 2:
    if all([author.name == Config.ADMIN_ID, message.channel.id == Config.ADMIN_CHANNEL_ID]):
      await admin_router(message, content_split)
    return
  
  # アドミンサーバーの場合
  if message.guild.id == Config.ADMIN_GUILD_ID: return
  
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
  
  # コマンドがあるかの判定 & コマンドの実行
  if content_split[0] == "observer" and len(content_split) >= 2:
    await router(message, content_split)
  elif content_split[0] == "observer":
    embed = Embed.make_embed("red", "無効なコマンドです。\n`observer help`でヘルプを表示できます。")
    await message.channel.send(embed = embed)

def main():
  # Botの起動とDiscordサーバーへの接続
  try:
    discord_client.run(Config.OBSERVER_TOKEN)
  finally: # サーバーを閉じた時（Ctrl + C）に動く処理
    database.close()
    print("Log out : Observer")

main()