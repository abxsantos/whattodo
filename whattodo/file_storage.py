"""Main module to handle data persistance using a json file."""
import json


def store_to_json(data):
    """
    Wrapper used to write data into json format.
    """
    with open("whattodo_data.json", "w+", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def read_from_json():
    """
    Wrapper used to read data into json format.
    """
    with open("whattodo_data.json", "r") as json_file:
        data = json.load(json_file)
    return data
