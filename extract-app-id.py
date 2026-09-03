import os
from dotenv import load_dotenv

load_dotenv()

import requests
import time

URL = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
MAX_RESULTS = 50000

def main() :
    last_app_id = 10
    stored_data : list[tuple[int, str]] = []
    while last_app_id is not None :
        print("Last_app_id :", last_app_id)
        app_ids, last_app_id = get_app_ids(last_app_id)
        stored_data = merge_data(app_ids, stored_data) 
        time.sleep(2)
    save_to_csv(stored_data, "data/steam_app_ids_list.csv")

def get_app_ids(last_app_id = None, max_results = MAX_RESULTS) :
    url = URL
    if max_results > 0 and max_results <= MAX_RESULTS :
        url = url + f"?max_results{max_results}"
    if last_app_id is not None :
        url = url + f"&last_appid={last_app_id}"
    result = requests.get(
        url,
	    headers={"x-webapi-key": os.getenv("STEAM_WEB_API_KEY")},
        timeout=20
    )

    result.raise_for_status()

    json_response = result.json()

    try :
        new_last_app_id = json_response["response"]["last_appid"]
    except :
        new_last_app_id = None

    app_ids = json_response["response"]["apps"]

    return app_ids, new_last_app_id


def merge_data(app_ids : list[dict], merged_data = list()) -> list[tuple[int, str]] :
    new_appids = [(app["appid"], app["name"]) for app in app_ids]
    merged_data = merged_data + new_appids
    return merged_data

def save_to_csv(data : list[tuple[int, str]], output_path = "data/data.csv", sep=";") -> None :
    with open(output_path, "w", encoding="UTF-8") as f :
        f.write(f"App ID{sep} Name\n")
        for app_id, name in data :
            f.write(f"{app_id}{sep}{name}\n")

if __name__ == "__main__" :
    main()