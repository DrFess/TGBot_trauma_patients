import json


def read_json(path_file: str) -> dict:
    with open(path_file) as file:
        return json.load(file)
