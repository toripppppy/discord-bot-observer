import discord

def make_embed(color = "white", description = "") -> discord.Embed:
  # Embedのカラー
  COLOR_DICT = {
    "white": 0xF0F0FF,
    "yellow": 0xFFFF00,
    "red": 0xFF0000,
    "green": 0x00FF00
  }
  
  embed = discord.Embed(title = "Observer")
  
  if color in COLOR_DICT.keys():
    embed.color = COLOR_DICT[color]
  else:
    embed.color = COLOR_DICT["white"]
    print(f"Warning: color '{color}' not found.")
  
  embed.description = description

  return embed