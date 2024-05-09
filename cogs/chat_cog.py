from discord.ext import commands

from others import Embed, Utils

"""
ChatCog
チャット関連の機能をまとめたCog
"""
class ChatCog(commands.Cog):
	def __init__(self, bot, database):
		self.bot = bot
		self.database = database

	# メッセージ受信時に動作する処理
	@commands.Cog.listener()
	async def on_message(self, message):
		author = message.author
		content = message.content
		
		# メッセージが空（写真）の場合
		if not content: return
		# Botだった場合
		if author.bot: return
		
		# メッセージ送信をした際のデータベース処理
		self.database.chat(author.name, content)
		data = self.database.get_data(author.name)
		level_up_cnt = Utils.get_level_up_cnt(data.level, data.chat, data.length)
		if level_up_cnt > 0: # レベルアップした場合
			self.database.update_level(author.name, level_up_cnt)
			embed = Embed.make_embed("green", f"{author.name}がレベルアップしました！（Lv:{data.level} → Lv:{data.level+level_up_cnt}）")
			await message.channel.send(embed = embed)
		self.database.log()

		# コマンドを実行 存在しなければエラー
		ctx = await self.bot.get_context(message)
		if ctx.command is None and content.startswith(self.bot.command_prefix):
			embed = Embed.make_embed("red", description="無効なコマンドです。\n`observer help`でヘルプを表示できます。")
			await message.channel.send(embed = embed)


	# 指定のユーザーデータを表示
	@commands.command(name="data", brief="<user>に該当する人のデータを表示します")
	async def data(self, message, user):
		data = self.database.get_data(user)
		if data:
			embed = Utils.create_data_embed(data)
		else:
			# 指定のユーザーが見つからない場合はエラー
			embed = Embed.make_embed("red", f"「{user}」のデータは見つかりませんでした。")

		await message.channel.send(embed = embed)

	# ユーザーデータを全て表示
	@commands.command(name="data-all", brief="すべての人のデータを表示します")
	async def data_all(self, message: commands.Context):
		for member in message.guild.members:
			# Botだった場合
			if member.bot: continue
			# data関数を呼び出す
			await self.data(message, member.name)

	# チャットランキングを表示
	@commands.command(name="chat-ranking", brief="チャット数ランキングを表示します")
	async def chat_ranking(self, message):
		chat_data = self.database.get_chat_ranking()
		await message.channel.send(embed = Utils.create_chat_ranking_embed(chat_data))

	# メンバー一覧を表示
	@commands.command(name="member", brief="サーバーのメンバーを表示します")
	async def member(self, message):
		await message.channel.send(embed = Utils.create_member_list_embed(message))