from pymongo import MongoClient

class Database:
  def __init__(self, URI, db_name, col_name):
    self.mongo_client = MongoClient(URI)
    self.database = self.mongo_client[db_name]
    self.collection = self.database[col_name]
    print("Database loading complete!!")
    self.log()
  
  def chat(self, author): # number-of-messageを増やす
    query = {"name": author}
    self.collection.update_one(query, {"$inc": {"number-of-message": 1}})
  
  def update_level(self, author, ):
    query = {"name": author}
    self.collection.update_one(query, {"$inc": {"level": 1}})
  
  def return_data(self, author):
    query = {"name": author}
    data = self.collection.find_one(query)
    if data == None:
      return None
    else:
      return data
  
  def return_level(self, author):
    data = self.return_data(author)
    if data == None:
      return None
    else:
      return data["level"]
  
  def return_number_of_message(self, author):
    data = self.return_data(author)
    if data == None:
      return None
    else:
      return data["number-of-message"]
  
  def return_chat_ranking(self) -> dict:
    data = self.find()
    chat_data = dict()
    for d in data:
      chat_data[d["name"]] = d["number-of-message"]
    
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