import json
import os

import requests
from icecream import ic

# <<<<<<< HEAD
GITHUB_JSON = "https://raw.githubusercontent.com/DominikOcsofszki/repo/refs/heads/main/"


def write_hover_items_to_file(data: str, name: str):
    JSON_FILES = os.path.join(os.path.dirname(__file__), "")
    with open(f"{JSON_FILES}{name}", "w", encoding="utf-8") as f:
        parsed_data = json.loads(data)
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)


def list_all_downloads():
    # <<<<<<< HEAD
    GITHUB_JSON_ALL = "https://raw.githubusercontent.com/DominikOcsofszki/repo/refs/heads/main/all.json"
    # =======
    #     GITHUB_JSON_ALL = "https://raw.githubusercontent.com/DominikOcsofszki/repo/refs/heads/main/json/all.json"
    # >>>>>>> 7c3089a04d6b30ba48a1d5c405e06232b29e3b49
    r = requests.get(f"{GITHUB_JSON_ALL}")
    json_content = r.content.decode("utf-8")
    parsed_data = json.loads(json_content)
    return parsed_data.get("all")


def load_from_github(file_name):
    # <<<<<<< HEAD
    ic(file_name)
    r = requests.get(f"{GITHUB_JSON}{file_name}")
    json_content = r.content.decode("utf-8")
    # =======
    #     GITHUB_JSON = (
    #         "https://raw.githubusercontent.com/DominikOcsofszki/repo/refs/heads/main/json/"
    #     )
    #     r = requests.get(f"{GITHUB_JSON}{file_name}")
    #     json_content = r.content.decode("utf-8")
    #     ic(json_content)
    # >>>>>>> 7c3089a04d6b30ba48a1d5c405e06232b29e3b49

    write_hover_items_to_file(json_content, file_name)


# <<<<<<< HEAD
def update_all_hover(update):
    if update:
        lst = list_all_downloads()
        # ic(lst)
        for file_name in lst:
            print("=================")
            print(f"ADD {file_name} from {GITHUB_JSON}")
            print("=================")
            load_from_github(file_name)


lst = list_all_downloads()
ic(lst)
print(load_from_github(lst[0]))
# =======
# lst = list_all_downloads()
# ic(lst)
# for file_name in lst:
#     load_from_github(file_name)
# >>>>>>> 7c3089a04d6b30ba48a1d5c405e06232b29e3b49
