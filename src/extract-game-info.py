import os
from dotenv import load_dotenv

load_dotenv()

import requests
import time
import json

BASE_URL = "https://store.steampowered.com/api/appdetails?appids="
OUTPUT_FILE = "data/games.json"

def get_game_info(app_id : int) -> dict :
    url = BASE_URL + str(app_id)
    result = requests.get(url)
    result.raise_for_status()
    json_content = result.json()
    game_info = json_content[str(app_id)]["data"]
    return game_info

def clean_game_info(game_info : dict) -> dict :
    keys_to_delete = ["header_image", "capsule_image", "capsule_imagev5", "background", "background_raw", "screenshots", "movies", "achievements", "support_info"]
    cleaned_info = {k: v for k, v in game_info.items() if k not in keys_to_delete}
    return cleaned_info

def save_game_info_to_file(game_info : dict, output_dir = "data/") -> bool :
    isFile = os.path.isfile(OUTPUT_FILE)
    if not isFile : 
        with open(OUTPUT_FILE, "w") as file :
            file_content : dict[str, list[dict]]= {
                "games" : []
            }
            file_content["games"].append(game_info)
            json.dump(file_content, file)
        return True
    else :
        content = None
        with open(OUTPUT_FILE, "r") as file :
            content = json.load(file)
            if not content :
                content : dict[str, list[dict]]= {
                    "games" : []
                }
            else :
                existing_games = content["games"]
                current_app_ids = []
                for game in existing_games :
                    app_id = game["steam_appid"]
                    current_app_ids.append(app_id)
                new_appid = game_info["steam_appid"]
                if new_appid in current_app_ids :
                    return False
            content["games"].append(game_info)

        with open(OUTPUT_FILE, "w") as file : 
            if content : 
                json.dump(content, file)
                return True

def main() :
    app_ids = [440, 730, 550]
    for app_id in app_ids :
        game_info = get_game_info(app_id)
        cleaned_info = clean_game_info(game_info)
        save_game_info_to_file(cleaned_info)
        time.sleep(0.5)


if __name__ == "__main__" :
    main()