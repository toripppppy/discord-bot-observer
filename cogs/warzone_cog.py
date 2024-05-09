from discord.ext import commands

"""
WarzoneCog
WARZONE!するためだけのCog
"""
class WarzoneCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# WARZONE!
	@commands.command(name="WARZONE!", brief="WARZONE!")
	async def warzone(self, ctx: commands.Context):
		"""
		observer WARZONE
		---
		WARZONE!
		"""
		await ctx.send("# WARZONE!\nhttps://youtu.be/uPySC2jFwhk")
