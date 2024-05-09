from discord.ext import commands

from others import Embed
import Config

"""
AdminCog
アドミン関連の機能をまとめたCog
"""
class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# アドミンコマンドのルーティング
	@commands.command(name="admin", hidden=True)
	async def admin_router(self, ctx, arg = None):
		# 引数の指定がない場合は無視
		# TODO embedを出すべき
		if arg is None:
			return

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
			channel = self.bot.get_channel(Config.BOT_LOG_CHANNEL_ID)
			await channel.send(embed = embed)
			await self.bot.close()