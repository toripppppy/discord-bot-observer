from pymongo import MongoClient
from others import Data

class Database:
  def __init__(self, URI, db_name, col_name):
    self.mongo_client = MongoClient(URI)
    self.database = self.mongo_client[db_name]
    self.collection = self.database[col_name]
    print("Database loading complete!!")
    self.log()
  
  def chat(self, author, content): # chatとlengthを更新
    query = {"name": author}
    self.collection.update_one(query, {"$inc": {"chat": 1}})
    
    if "https://" in content or "http://" in content: return # URLが含まれていた場合
    if "```" in content: return                              # コードブロックが含まれていた場合
    
    self.collection.update_one(query, {"$inc": {"length": len(content)}})
  
  def update_level(self, author, level_up_cnt):
    query = {"name": author}
    self.collection.update_one(query, {"$inc": {"level": level_up_cnt}})
  
  def return_data(self, author) -> Data:
    query = {"name": author}
    data = self.collection.find_one(query)
    if data is None:
      print(f"Error: Data is None. Does '{author}' exist?")
    else:
      return Data(
        name=data["name"],
        point=data["point"],
        level=data["level"],
        chat=data["chat"],
        length=data["length"]
      )
  
  def return_level(self, author):
    data = self.return_data(author)
    if data == None:
      return None
    else:
      return data.level
  
  def return_chat(self, author):
    data = self.return_data(author)
    if data == None:
      return None
    else:
      return data.chat
  
  def return_length(self, author):
    data = self.return_data(author)
    if data == None:
      return None
    else:
      return data.length
  
  def return_chat_ranking(self) -> dict:
    data = self.find()
    chat_data = dict()
    for d in data:
      chat_data[d["name"]] = d["chat"]
    
    return chat_data
  
  def log(self):
    print("=" * 60, self.collection.name, "=" * 60)
    for data in self.collection.find():
      print(data)
    print("=" * (120 + 2 + len(self.collection.name)), flush = True)
  
  def close(self):
    self.mongo_client.close()
  
  def find(self, query = {}):
    if query == {}:
      return self.collection.find()
    else:
      return self.collection.find(query)