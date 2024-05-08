from others import Embed

class ErrorManager:
  """
  エラーコードからエラーを生成する
  """
  def __init__(self, error_code) -> None:
    self.error_code = error_code

  
  def make_error_embed(self, data: object):
    desc = ""
    if self.error_code == "udiq.cannot_find_specified_key":
      desc = f'key \'{data["key"]}\' が見つかりませんでした。'

    embed = Embed.make_embed("red", desc)
    return embed