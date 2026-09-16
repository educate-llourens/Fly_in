from argparse import ArgumentParser, Namespace
from pathlib import Path
from src.classes import (FlyInSettings, InputError, ParsingError, Hub,
                         Connection, Zone)
from rich.errors import StyleSyntaxError
from sys import argv

# Functions in ----------------------------------------------------------------
# 1. parsing
# 2. parse_file
# 3. extract_hub_info
# 4. extract_connection
# 5. find_hub
# -----------------------------------------------------------------------------


def parsing() -> FlyInSettings:
    """Handles the parsing of the information.

    Raises:
        InputError: If the file is not the only argument

    Returns:
        FlyInSettings: Instance of overall settings information
    """
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
    """Parses the map file and distributes the information into their
    appropriate classes.

    Args:
        file_path (str): Path to map file
        settings (FlyInSettings): Instance of the overall settings
        information

    Raises:
        ParsingError: More than one start hub detected
        ParsingError: More than one end hub detected

    Returns:
        FlyInSettings: Instance of the overall settings
    """

    with open(file_path, "r") as config_file:
        for line in config_file:
            line = line.strip()
            if line.startswith("nb_drones"):
                settings.nbr_drones = int(line.split(":", 1)[1])
            elif line.startswith("start_hub"):
                if settings.start_hub.name:
                    raise ParsingError(f"{line} | Duplicate start hub")
                settings.start_hub = extract_hub_info(line)
                settings.hubs_list.insert(0, settings.start_hub)
            elif line.startswith("hub"):
                settings.hubs_list.append(extract_hub_info(line))
            elif line.startswith("end_hub"):
                if settings.end_hub.name:
                    raise ParsingError(f"{line} | Duplicate end hub")
                settings.end_hub = extract_hub_info(line)
                settings.hubs_list.insert(
                    len(settings.hubs_list), settings.end_hub)
            elif (line.startswith("connection")):
                connection: Connection = extract_connection(
                    line, settings.hubs_list)
                settings.connections_list.append(connection)
    return settings


def extract_hub_info(line: str) -> Hub:
    """Extracts the information for the hub and sticks it in the hub instance

    Args:
        line (str): The line from the map file that wer are parsing

    Raises:
        ParsingError: If hub coordinates are invalid

    Returns:
        Hub: A hub instance
    """
    get_info_str: str
    info_list: list[str]
    meta_data_list: list[str]
    meta_data: Hub.MetaData | None = None

    get_info_str = line.split(": ")[1]
    info_list = get_info_str.split(" ", 3)
    name = info_list[0]
    try:
        x = int(info_list[1])
        y = int(info_list[2])
    except ValueError:
        raise ParsingError(f"Invalid coordinates for {name}")
    if info_list[3]:
        meta_data_list = info_list[3].split(" ")
        for data in meta_data_list:
            if meta_data is None:
                meta_data = Hub.MetaData()
            if "color" in data:
                try:
                    meta_data.colour = (
                        data.split("color=")[1].replace("]", ""))
                except StyleSyntaxError:
                    raise ParsingError(f"Invalid colour for {name}")
            if "zone" in data:
                zone_str: str = (
                    data.split("zone=")[1].replace("]", ""))
                try:
                    meta_data.zone = Zone(zone_str)
                except ValueError:
                    raise ParsingError(f"Invalid zone for {name}")
            if "max_drones" in data:
                meta_data.max_drones = (
                    int(data.split("max_drones=")[1].replace("]", "")))
    new_hub = Hub(name=name, x=x, y=y, meta_data=meta_data)
    return new_hub


def extract_connection(line: str, hubs_list: list[Hub]) -> Connection:
    """Extracts information for the connection

    Args:
        line (str): Line being parsed
        hubs_list (list[Hub]): List of hub instances

    Returns:
        Connection: A connection instance
    """
    connections: str = line.split(": ", 1)[1]
    get_connections_list: list[str] = connections.split(" ")
    connections_list: list[str] = (
        get_connections_list[0].split("-"))
    connection_hubs_list: list[Hub] = []
    for i in range(len(connections_list)):
        hub = find_hub(hubs_list, connections_list[i])
        connection_hubs_list.append(hub)
    hubs_tuple = (connection_hubs_list[0], connection_hubs_list[1])
    max_link_capacity = 1
    if len(get_connections_list) > 1:
        connections_metadata: str = get_connections_list[1]
        max_link_capacity = int(
            connections_metadata.split(
                "max_link_capacity=")[1].replace("]", ""))
    connection = Connection(
        hubs_list=hubs_tuple, max_link_capacity=max_link_capacity)
    return connection


def find_hub(hubs_list: list[Hub], hub_name: str) -> Hub:
    for hub in hubs_list:
        if hub.name == hub_name:
            return hub
    raise ParsingError("Could not find hub in find_hub")
