import json


def get_data(
    key: str,
    file: str = "settings.json"
):
    with open(file, "r") as f:
        data = json.load(f)
        return data[key]


def get_dest_channels():
    with open("settings.json", "r") as f:
        data = json.load(f)
        return data["destination_channels"]


def get_allow_list():
    with open("settings.json", "r") as f:
        data = json.load(f)
        return data["allow_list"]
