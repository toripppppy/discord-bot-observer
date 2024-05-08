from pymongo import MongoClient
from pymongo.cursor import Cursor

import random

UDIQ_PATH = "data/udiq.json"

class Knowledge:
  def __init__(self, word: str, meaning: str) -> None:
    self.word = word
    self.meaning = meaning

  def __str__(self) -> str:
    return f"<{self.word} : {self.meaning}>"


class UdiqController:
  """
  observer udiq
  ---
  {
    key: Knowledge
  }
  の形で対応している
  """
  def __init__(self, URI: str, db_name: str, col_name: str):
    # MongoDB
    self.mongo_client = MongoClient(URI)
    self.database = self.mongo_client[db_name]
    self.collection = self.database[col_name]
    # udiqを最初に一回読み込む
    self.udiq = dict()
    self.load_udiq()
    # 読み込み完了を通知
    print("udiq loaded")


  ### データベース関連
  def load_udiq(self) -> None:
    """
    self.udiqにudiqを読み込む
    """
    self.udiq = self.parse_db_udiq(self.get_db_udiq())


  def get_db_udiq(self) -> dict[str, str]:
    """
    MongoDBからudiqを取得する
    """
    db_udiq = self.collection.find()
    return db_udiq
  

  def parse_db_udiq(self, db_udiq: Cursor) -> dict[str, Knowledge]:
    """
    Cursor型のudiqをdictにする
    """
    udiq = dict()
    for data in db_udiq:
      knowledge = Knowledge(data.get("word"), data.get("meaning"))
      # 要素が不足している場合は無視
      if knowledge.word is None or knowledge.meaning is None:
        continue
      # key: Knowledge の形に整形
      udiq.update({knowledge.word : knowledge})
      
    return udiq
  

  def update_db_udiq_record(self, knowledge: Knowledge):
    """
    MongoDBの指定されたデータを更新する
    """
    # keyに対応するものが存在するならupdate、無ければinsert
    if self.get_knowledge(knowledge.word):
      self.collection.update_one({"word": knowledge.word}, {'$set':{'meaning': knowledge.meaning}})

    else:
      self.collection.insert_one({"word": knowledge.word, "meaning": knowledge.meaning})


  def delete_db_udiq_record(self, key: str) -> Knowledge | None:
    """
    MongoDBの指定されたデータを削除する
    """
    knowledge = self.get_knowledge(key)

    if knowledge:
      self.collection.delete_one({"word": key})
      return knowledge
    else:
      # keyが見つからない
      return None


  ### botとのインターフェース
  def get_udiq(self) -> dict[str, Knowledge]:
    """
    UdiqControllerのudiqを返す
    """
    return self.udiq


  def get_knowledge(self, key: str) -> Knowledge:
    """
    UdiqControllerからkeyに対応したknowledgeを返す
    対応するものがなければNone
    """
    meaning = self.udiq.get(key)

    if meaning is not None:
      return Knowledge(key, meaning)
    else:
      return None
    

  def get_random_knowledge(self) -> Knowledge:
    """
    ランダムなKnowledgeを返す
    """
    udiq = self.get_udiq()
    knowledge = random.choice(list(udiq.values()))
    return knowledge
    

  def append_knowledge(self, word: str, meaning: str) -> Knowledge:
    """
    {word : meaning}の組を新しく登録する
    keyが被ったら重複せずに更新する
    """
    new_knowledge = Knowledge(word, meaning)
    # UdiqControllerのudiqを更新
    self.udiq.update({new_knowledge.word : new_knowledge})

    return new_knowledge