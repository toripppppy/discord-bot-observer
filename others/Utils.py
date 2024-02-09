from unicodedata import east_asian_width # 全角半角判定用
from math import isqrt
from others import Data

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

def create_data_text(data: Data):
  """
  整形した表示データを返す
  """
  text = str()
  text += f"========== {data.name} ==========\n"
  text += f"・現在のポイント：{data.point}\n"
  text += f"・現在のレベル　：{data.level}\n"
  text += f"・合計チャット数：{data.chat}\n"
  text += f"・合計文字数　　：{data.length}\n"
  text += "="* (20 + len(data.name))

  return text