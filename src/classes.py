from sys import argv


class FlyInSettings:
    def __init__(self) -> None:
        if len(argv) != 2:
            raise InputError("Takes ony the map config file as an argument")
        self.read_and_format()

    def read_and_format(self) -> None:
        with open(argv, "r") as map_config_file:
            for line in map_config_file:
                if line.startswith("#"):
                    self.map_description: str = line.split("# ", 1)[1]
                elif line.startswith("nb_drones"):
                    self.nbr_drones: int = int(line.split(": ", 1)[1])
                elif line.startswith("start_hub"):
                    start_line: str = line.split(": ")[1]
                    start_info: list[str] = start_line.split(" ")
                    self.start_x: int = int(start_info[1])
                    self.start_y: int = int(start_info[2])
                    self.start_metadata: str = start_info[3]
                elif line.startswith("end_hub"):
                    end_line: str = line.split(": ")[1]
                    end_info: list[str] = end_line.split(" ")
                    self.end_x: int = int(end_info[1])
                    self.end_y: int = int(end_info[2])
                    self.end_metadata: str = end_info[3]
                elif line.startswith("hub"):


class Hub:
    def __init__(self, line: str) -> None:
        self.name


class InputError:
    def __init__(self, msg: str) -> None:
        super().__init__(f"Input Error: {msg}")
