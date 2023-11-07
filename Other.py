from unicodedata import east_asian_width # 全角半角判定用
from math import isqrt

def check_width(string) -> int:
  "全角の文字を2文字としてカウントした文字数を返す"
  count = 0
  for char in string:
    if east_asian_width(char) in "FWA":
      count += 2
    else:
      count += 1
  return count

def check_update_level(level, number_of_message) -> bool:
  if level != isqrt(number_of_message):
    return True
  else:
    return False