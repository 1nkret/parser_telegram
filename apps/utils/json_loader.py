import json


def get_dest_channels() -> dict:
    with open("settings.json", "r") as f:
        data = json.load(f)
        return data["destination_channels"]


def get_allow_list() -> list:
    with open("settings.json", "r") as f:
        data = json.load(f)
        return data["allow_list"]
