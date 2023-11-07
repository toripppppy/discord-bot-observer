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

def reset_number_of_message():
  author = input("author: ")
  if author == "all":
    database.collection.update_many({}, {"$set": {"number-of-message": 0}})
  elif author in Data.ID_LIST:
    database.collection.update_one({"name": author}, {"$set": {"number-of-message": 0}})
  else:
    print("IDが見つかりませんでした。")
  database.log()

def main():
  do_reset_level = input("reset_level()(y/n): ")
  if do_reset_level == "y":
    reset_level()
  
  do_message = input("reset_number_of_message()(y/n): ")
  if do_message == "y":
    reset_number_of_message()

main()