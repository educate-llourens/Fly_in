from src.classes import FlyInSettings, InputError, Hub
from sys import argv


def parsing() -> FlyInSettings:
    settings: FlyInSettings = FlyInSettings()

    if len(argv) != 2:
        raise InputError("The program only takes the config file as "
                         "an argument")
    with open(argv[1], "r") as config_file:
        for line in config_file:
            if line.startswith("#"):
                settings.description = line.split("#")[1]
            elif line.startswith("start_hub"):
                settings.hubs_list[0]: Hub = extract_hub_info(line)
    return settings


def extract_hub_info(line: str) -> Hub:
    new_hub: Hub
    get_info_str: str
    info_list: list[str]
    meta_data_list: list[str]

    get_info_str = line.split(": ")[1]
    info_list = get_info_str.split(" ")
    new_hub = Hub()
    new_hub.name = info_list[0]
    new_hub.x = info_list[1]
    new_hub.y = info_list[2]
    if info_list[3]:
        info_list[3].replace("[", "")
        info_list[3].replace("]", "")
        meta_data_list = info_list[3].split(" ")
        for data in meta_data_list:
            if "color" in data:
                new_hub.meta_data.colour = data.split("color=")[1]
    return new_hub
