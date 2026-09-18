from pydantic import BaseModel, ConfigDict, Field, model_validator
from sys import maxsize
from collections import Counter
from rich.style import Style
from enum import Enum
from src.error_handling import ParsingError

# Classes list ----------------------------------------------------------------
# 1. FlyInSettings
# 2. Hub
#    a. Metadata
# 3. Connection
# 4. InputError
# 5. ParsingError
# -----------------------------------------------------------------------------


class FlyInSettings(BaseModel):
    """Creates the overview settings class.
    """
    nbr_drones: int = Field(default=maxsize, gt=0)
    drones_list: list["Drone"] = Field(default_factory=list)
    hubs_list: list["Hub"] = Field(default_factory=list)
    start_hub: "Hub" = Field(default_factory=lambda: Hub())
    end_hub: "Hub" = Field(default_factory=lambda: Hub())
    connections_list: list["Connection"] = Field(default_factory=list)

    @model_validator(mode="after")
    def settings_validation(self) -> "FlyInSettings":
        # Duplicate names -------------------------------------------
        names_list: list[str] = [hub.name for hub in self.hubs_list]
        counter: Counter = Counter(names_list)
        duplicate_hub_names: list[str] = [
            name for name, count in counter.items() if count > 1]
        if len(duplicate_hub_names) > 0:
            raise ParsingError(f"Duplicate names for {duplicate_hub_names}. "
                               "Please remove all duplicates")
        # Duplicate connections -------------------------------------
        connections_name_list: list[tuple[str, str]] = []
        for connection in self.connections_list:
            connections_name_list.append((connection.connection_start_hub.name,
                                          connection.connection_end_hub.name))
        counter = Counter(connections_name_list)
        duplicate_connections_list: list[tuple[str, str]] = [
            connection for connection, count in counter.items() if count > 1
        ]
        if len(duplicate_connections_list) > 0:
            raise ParsingError(
                f"Duplicate connections for {duplicate_connections_list}. "
                "Please remove all duplicates")
        # Start and end hub no max drone limit ----------------------
        if self.start_hub.meta_data:
            if self.start_hub.meta_data.max_drones:
                self.start_hub.meta_data.max_drones = maxsize
        if self.end_hub.meta_data:
            if self.end_hub.meta_data.max_drones:
                self.end_hub.meta_data.max_drones = maxsize
        # Drone_id's correct ----------------------------------------
        for drone in self.drones_list:
            if drone.id == maxsize and len(self.drones_list) + 1 < maxsize:
                raise ParsingError(f"Drone id {maxsize} should be less than "
                                   f"{self.nbr_drones}")
        return self

    def create_drones(self) -> None:
        for i in range(self.nbr_drones - 1):
            self.drones_list.append(Drone(id=i + 1))


class Zone(Enum):
    normal = "normal"
    blocked = "blocked"
    restricted = "restricted"
    priority = "priority"


class Hub(BaseModel):
    """Settings information for the hubs
    name
    """
    class MetaData(BaseModel):
        """Metadata for the hub
        """
        model_config = ConfigDict(arbitrary_types_allowed=True)
        zone: Zone = Field(default=Zone.normal)
        colour: str = Field(default="default")
        print_style: Style = Field(
            default_factory=lambda: Style.parse("default"))
        max_drones: int = Field(default=1, ge=0)

        @model_validator(mode="after")
        def set_print_style(self):
            if self.colour == "orange":
                self.print_style = Style.parse("orange1")
            else:
                self.print_style = Style.parse(self.colour)
            return self

    name: str = Field(default="")
    x: int = Field(default=(maxsize), ge=0)
    y: int = Field(default=maxsize, ge=0)
    meta_data: MetaData | None = Field(default=None)

    @model_validator(mode="after")
    def hub_validation(self) -> "Hub":
        # Valid Hub name --------------------------------------------
        for chr in self.name:
            if not chr.isprintable() or chr == " " or chr == "-":
                raise ParsingError(f"{self.name} is not a valid hub name")
        return self


class Connection(BaseModel):
    """Settings information for the Connection
    """
    connection_start_hub: Hub = Field(default_factory=lambda: Hub())
    connection_end_hub: Hub = Field(default_factory=lambda: Hub())
    max_link_capacity: int | None = Field(default=None, ge=0)


class Drone(BaseModel):
    id: int = Field(default=maxsize, ge=0)
