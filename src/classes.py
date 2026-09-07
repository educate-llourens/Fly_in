# Classes list ----------------------------------------------------------------
# 1. FlyInSettings
# 2. Hub
#    a. Metadata
# 3. Connection
# 4. InputError
# 5. ParsingError
# -----------------------------------------------------------------------------


class FlyInSettings:
    def __init__(self) -> None:
        self.nbr_drones: int = 0
        self.hubs_list: list[Hub] = []
        self.start_hub: Hub = Hub()
        self.end_hub: Hub = Hub()
        self.connections_list: list[Connection] = []


class Hub:
    def __init__(self) -> None:
        self.name: str = ""
        self.x: int = 0
        self.y: int = 0
        self.meta_data: self.MetaData = self.MetaData()

    class MetaData:
        def __init__(self) -> None:
            self.zone: str = "normal"
            self.colour: str = "None"
            self.max_drones: int = 0


class Connection:
    def __init__(self) -> None:
        self.hubs_list: list[Hub] = []
        self.max_link_capacity: int = 1


class InputError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Input Error: {msg}")


class ParsingError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Parsing Error: {msg}")
