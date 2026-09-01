from classes import FlyInSettings, InputError, Hub, Connection
from sys import argv


def parsing() -> FlyInSettings:
    settings: FlyInSettings = FlyInSettings()

    if len(argv) != 2:
        raise InputError("The program only takes the config file as "
                         "an argument")
    with open(argv[1], "r") as config_file:
        for line in config_file:
            if line.startswith("nb_drones"):
                settings.nbr_drones = int(line.split(":", 1)[1])
            elif line.startswith("start_hub"):
                settings.start_hub = extract_hub_info(line)
            elif line.startswith("hub"):
                settings.hubs_list.append(extract_hub_info(line))
            elif line.startswith("end_hub"):
                settings.end_hub = extract_hub_info(line)
            elif (line.startswith("connection")):
                connections: str = line.split(": ", 1)[1]
                connections_list: list[str] = connections.split("-")
                for i in range(len(connections_list)):
                    for j in range(len(settings.hubs_list)):
                        if connections_list[i] == settings.hubs_list[j].name:
                            set_connection: Connection = Connection()
                            set_connection.connections.append(
                                (settings.hubs_list[j]))
                            print(settings.connections_list)
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
    new_hub.x = info_list[1]
    new_hub.y = info_list[2]
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
