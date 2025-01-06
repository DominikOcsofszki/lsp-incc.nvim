import json
import os

from icecream import ic

# <<<<<<< HEAD
from incc_lsp.CONFIGS import UPDATE_JSON_FROM_GITHUB
from incc_lsp.lsp_text_import_hover import load_from_github

# =======
#
# def load_hover_items_from_file(__hover_tasks_json_file: str):
#     with open(file=f"{__hover_tasks_json_file}", mode="r") as f:
#         hover_tasks: dict[str, str] = json.loads(f.read())
#     return_item = hover_tasks
#     return return_item
#
#
# def get_all_files_in_json_folder(json_folder):
#     from os import listdir
#
#     all_files_abs_paths = [
#         f"{json_folder}{json_file}" for json_file in listdir(json_folder)
#     ]
#     return all_files_abs_paths
#
#
# def load_all_hover(all_hover_files: list[str]):
#     __hover_dict: dict[str, str] = {}
#     for json_file in all_hover_files:
#         json_data = load_hover_items_from_file(json_file)
#         __hover_dict.update(json_data)
#     return __hover_dict
#
#
# JSON_FOLDER = "/Users/dominik/HOME/BA/DEV/MAIN/src/incc_lsp/lsp_text_import/json/"
# __all_hover_files = get_all_files_in_json_folder(JSON_FOLDER)
#
# __hover_dict = load_all_hover(__all_hover_files)
# >>>>>>> 7c3089a04d6b30ba48a1d5c405e06232b29e3b49


def __load_hover_items_from_file(__hover_tasks_json_file: str):
    with open(file=f"{__hover_tasks_json_file}", mode="r") as f:
        hover_tasks: dict[str, str] = json.loads(f.read())
    return_item = hover_tasks
    return return_item


def __get_all_files_in_json_folder(json_folder):
    from os import listdir

    all_files_abs_paths = [
        f"{json_folder}{json_file}" for json_file in listdir(json_folder)
    ]
    return all_files_abs_paths


def __load_all_hover(all_hover_files: list[str]):
    __hover_dict: dict[str, str] = {}
    for json_file in all_hover_files:
        json_data = __load_hover_items_from_file(json_file)
        __hover_dict.update(json_data)
    return __hover_dict


def get_all_hover_from_folder(JSON_FOLDER: str):
    __all_hover_files = __get_all_files_in_json_folder(JSON_FOLDER)
    __hover_dict = __load_all_hover(__all_hover_files)
    hover_dict_lower_case = {k.lower(): v for k, v in __hover_dict.items()}
    return hover_dict_lower_case


def get_all_hover_items_from_json_files():
    # JSON_FOLDER = "/Users/dominik/HOME/BA/DEV/MAIN/src/incc_lsp/lsp_text_import/json/"
    JSON_FOLDER = os.path.join(os.path.dirname(__file__), "json/")

    return get_all_hover_from_folder(JSON_FOLDER)
    # __all_hover_files = __get_all_files_in_json_folder(JSON_FOLDER)
    # __hover_dict = __load_all_hover(__all_hover_files)
    # hover_dict_lower_case = {k.lower(): v for k, v in __hover_dict.items()}
    # return hover_dict_lower_case


def get_all_tasks_json_hover():
    # if UPDATE_JSON_FROM_GITHUB:
    #     load_from_github.update_all_hover()
    JSON_FOLDER = os.path.join(os.path.dirname(__file__), "tasks_json/")

    # JSON_FOLDER = (
    #     "/Users/dominik/HOME/BA/DEV/MAIN/src/incc_lsp/lsp_text_import/tasks_json/"
    # )
    return get_all_hover_from_folder(JSON_FOLDER)
    #
    # __all_hover_files = __get_all_files_in_json_folder(JSON_FOLDER)
    #
    # __hover_dict = __load_all_hover(__all_hover_files)
    #
    # hover_dict_lower_case = {k.lower(): v for k, v in __hover_dict.items()}
    # return hover_dict_lower_case


hover_dict_lower_case = get_all_hover_items_from_json_files()
