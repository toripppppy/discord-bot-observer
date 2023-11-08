import database_manager
import Data

database = database_manager.Database(Data.MONGODB_URI, "discord", "user-data")

def reset_level():
  author = input("author: ")
  if author == "all":
    database.collection.update_many({}, {"$set": {"level": 0}})
  elif author in Data.ID_LIST:
    database.collection.update_one({"name": author}, {"$set": {"level": 0}})
  else:
    print("IDが見つかりませんでした。")
  database.log()

def reset_chat():
  author = input("author: ")
  if author == "all":
    database.collection.update_many({}, {"$set": {"chat": 0}})
  elif author in Data.ID_LIST:
    database.collection.update_one({"name": author}, {"$set": {"chat": 0}})
  else:
    print("IDが見つかりませんでした。")
  database.log()

def reset_length():
  author = input("author: ")
  if author == "all":
    database.collection.update_many({}, {"$set": {"length": 0}})
  elif author in Data.ID_LIST:
    database.collection.update_one({"name": author}, {"$set": {"length": 0}})
  else:
    print("IDが見つかりませんでした。")
  database.log()

def main():
  do_reset_level = input("reset_level()(y/n): ")
  if do_reset_level == "y":
    reset_level()
  
  do_message = input("reset_chat()(y/n): ")
  if do_message == "y":
    reset_chat()
  
  do_length = input("reset_length()(y/n): ")
  if do_length == "y":
    reset_length()

main()