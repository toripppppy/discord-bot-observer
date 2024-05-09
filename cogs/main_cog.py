from discord.ext import commands

from others import Embed, Utils
import Config

"""
MainCog
どこにも属さない主要な機能をまとめたcog
"""
class MainCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# ヘルプ
	@commands.command(name="help", brief="ヘルプを表示します")
	async def help(self, message):
		await message.channel.send(embed = Utils.create_help_embed(self.bot))

	# 起動時に動作する処理
	@commands.Cog.listener()
	async def on_ready(self):
		print('Log in : Observer', flush = True)
		embed = Embed.make_embed("yellow", "起動しました。")
		channel = self.bot.get_channel(Config.BOT_LOG_CHANNEL_ID)
		await channel.send(embed = embed)