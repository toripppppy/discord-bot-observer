from unicodedata import east_asian_width # 全角半角判定用
from math import isqrt
import discord

def check_width(string) -> int:
  "全角の文字を2文字としてカウントした文字数を返す"
  count = 0
  for char in string:
    if east_asian_width(char) in "FWA":
      count += 2
    else:
      count += 1
  return count

def return_level_up_cnt(level, chat, length):
  new_level = isqrt(chat + (length // 10))
  return new_level - level


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