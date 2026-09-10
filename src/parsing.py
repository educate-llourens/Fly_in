from argparse import ArgumentParser, Namespace
from pathlib import Path
from src.classes import (FlyInSettings, InputError, ParsingError, Hub,
                         Connection)
from sys import argv, maxsize

# Functions in ----------------------------------------------------------------
# 1. parsing
# 2. parse_file
# 3. extract_hub_info
# 4. extract_connection
# 5. find_hub
# -----------------------------------------------------------------------------


def parsing() -> FlyInSettings:
    settings: FlyInSettings = FlyInSettings()

    if len(argv) > 2:
        raise InputError("The program only takes the config file as "
                         "an argument")
    parser = ArgumentParser()
    parser.add_argument(
        "map",
        default="maps/01_linear_path.txt"
    )
    args: Namespace = parser.parse_args()
    path_map = str(Path(args.map))
    settings = parse_file(path_map, settings)
    return settings


def parse_file(file_path: str, settings: FlyInSettings) -> FlyInSettings:
    start_hub_count: int = 0
    end_hub_count: int = 0

    with open(file_path, "r") as config_file:
        for line in config_file:
            line = line.strip()
            if line.startswith("nb_drones"):
                settings.nbr_drones = int(line.split(":", 1)[1])
            elif line.startswith("start_hub"):
                if start_hub_count == 1:
                    raise ParsingError("parse_file detected more than "
                                       "one start_hub")
                settings.start_hub = extract_hub_info(line)
                settings.hubs_list.insert(0, settings.start_hub)
                settings.start_hub.meta_data.zone = maxsize
                start_hub_count += 1
            elif line.startswith("hub"):
                settings.hubs_list.append(extract_hub_info(line))
            elif line.startswith("end_hub"):
                if end_hub_count == 1:
                    raise ParsingError("parse_file detected more than "
                                       "one end_hub")
                settings.end_hub = extract_hub_info(line)
                settings.hubs_list.insert(
                    len(settings.hubs_list), settings.end_hub)
                settings.end_hub.meta_data.max_drones = maxsize
                end_hub_count += 1
            elif (line.startswith("connection")):
                connection: Connection = extract_connection(
                    line, settings.hubs_list)
                settings.connections_list.append(connection)
    return settings


def extract_hub_info(line: str) -> Hub:
    new_hub: Hub
    get_info_str: str
    info_list: list[str]
    meta_data_list: list[str]

    get_info_str = line.split(": ")[1]
    info_list = get_info_str.split(" ", 3)
    new_hub = Hub()
    new_hub.name = info_list[0]
    try:
        new_hub.x = int(info_list[1])
        new_hub.y = int(info_list[2])
    except ValueError:
        raise ParsingError(f"Invalid coordinates for {new_hub.name}")
    if info_list[3]:
        meta_data_list = info_list[3].split(" ")
        for data in meta_data_list:
            if "color" in data:
                new_hub.meta_data.colour = (
                    data.split("color=")[1].replace("]", ""))
            if "zone" in data:
                new_hub.meta_data.zone = (
                    data.split("zone=")[1].replace("]", ""))
            if "max_drones" in data:
                new_hub.meta_data.max_drones = (
                    int(data.split("max_drones=")[1].replace("]", "")))
    return new_hub


def extract_connection(line: str, hubs_list: list[Hub]) -> Connection:
    connections: str = line.split(": ", 1)[1]
    get_connections_list: list[str] = connections.split(" ")
    connections_list: list[str] = (
        get_connections_list[0].split("-"))
    connection: Connection = Connection()
    for i in range(len(connections_list)):
        hub = find_hub(hubs_list, connections_list[i])
        connection.hubs_list.append(hub)
    if len(get_connections_list) > 1:
        connections_metadata: str = get_connections_list[1]
        connection.max_link_capacity = int(
            connections_metadata.split(
                "max_link_capacity=")[1].replace("]", ""))
    return connection


def find_hub(hubs_list: list[Hub], hub_name: str) -> Hub:
    for hub in hubs_list:
        if hub.name == hub_name:
            return hub
    raise ParsingError("Could not find hub in find_hub")
