import json
import os

from pymongo import MongoClient
from pymongo.collection import Collection

GAME_FILE_PATH = "data/games.json"

def main() :
    db = get_database()
    collection = get_collection(db, "indie-games")
    games = read_file()
    collection.insert_many(games)

def get_database() :
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client

def get_collection(db : MongoClient, collection : str) -> Collection :
    db_collection = db["local"][collection]
    return db_collection

def read_file(file_path=GAME_FILE_PATH) -> dict|None :
    def insert_id(game_info : dict) -> dict :
        app_id = game_info["steam_appid"]
        game_info["_id"] = app_id
        return game_info
    
    if not os.path.isfile(file_path) :
        return None
    
    with open(file_path, "r") as file :
        game_info = json.load(file)
        games = list(map(insert_id, game_info["games"]))
        return games

if __name__ == "__main__" :
    main()