import json


def read_from_json_file(filename: str):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def write_to_json_file(filename: str, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_user_library():
    return read_from_json_file("user_library/user_library.json")


def load_global_library():
    return read_from_json_file("data.json")


def save_user_library(data):
    write_to_json_file("user_library/user_library.json", data)
