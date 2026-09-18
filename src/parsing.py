from src.settings import (
    FlyInSettings, Hub, Connection, Zone)
from src.error_handling import ParsingError
from rich.errors import StyleSyntaxError

# Functions in ----------------------------------------------------------------
# 1. parsing
# 2. parse_file
# 3. extract_hub_info
# 4. extract_connection
# 5. find_hub
# -----------------------------------------------------------------------------


class Parser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.settings: FlyInSettings = FlyInSettings()

    def parse_file(self) -> FlyInSettings:
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

        with open(self.file_path, "r") as config_file:
            for line in config_file:
                line = line.strip()
                if line.startswith("nb_drones"):
                    self.settings.nbr_drones = int(line.split(":", 1)[1])
                elif line.startswith("start_hub"):
                    if self.settings.start_hub.name:
                        raise ParsingError(f"{line} | Duplicate start hub")
                    self.settings.start_hub = self.extract_hub_info(line)
                    self.settings.hubs_list.insert(0, self.settings.start_hub)
                elif line.startswith("hub"):
                    self.settings.hubs_list.append(self.extract_hub_info(line))
                elif line.startswith("end_hub"):
                    if self.settings.end_hub.name:
                        raise ParsingError(f"{line} | Duplicate end hub")
                    self.settings.end_hub = self.extract_hub_info(line)
                    self.settings.hubs_list.insert(
                        len(self.settings.hubs_list), self.settings.end_hub)
                elif (line.startswith("connection")):
                    connection: Connection = self.extract_connection(
                        line, self.settings.hubs_list)
                    self.settings.connections_list.append(connection)
        return self.settings

    def extract_hub_info(self, line: str) -> Hub:
        """Extracts the information for the hub and sticks it in the
        hub instance

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

    def extract_connection(self, line: str, hubs_list: list[Hub]
                           ) -> Connection:
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
            hub = self.find_hub(hubs_list, connections_list[i])
            connection_hubs_list.append(hub)
        connection_start_hub = connection_hubs_list[0]
        connection_end_hub = connection_hubs_list[1]
        max_link_capacity = 1
        if len(get_connections_list) > 1:
            connections_metadata: str = get_connections_list[1]
            max_link_capacity = int(
                connections_metadata.split(
                    "max_link_capacity=")[1].replace("]", ""))
        connection = Connection(
            connection_start_hub=connection_start_hub,
            connection_end_hub=connection_end_hub,
            max_link_capacity=max_link_capacity)
        return connection

    def find_hub(self, hubs_list: list[Hub], hub_name: str) -> Hub:
        for hub in hubs_list:
            if hub.name == hub_name:
                return hub
        raise ParsingError("Could not find hub in find_hub")
