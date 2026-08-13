class FlyInSettings:
    def __init__(self) -> None:
        self.description: str
        self.nbr_drones: int
        self.hubs_list: list[Hub]
        self.connections_list[Connection]


class Hub:
    def __init__(self, line: str) -> None:
        self.name: str
        self.x: int
        self.y: int
        self.meta_data: self.MetaData

    class MetaData:
        def __init__(self) -> None:
            self.zone: str = "normal"
            self.colour: str = "None"
            self.max_drones: int = 1


class Connection:
    def __init_(self, line: str) -> None:
        self.connection_a: Hub
        self.connection_b: Hub


class InputError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Input Error: {msg}")
