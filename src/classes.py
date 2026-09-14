from pydantic import BaseModel, Field, model_validator
from sys import maxsize
from collections import Counter

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
    hubs_list: list["Hub"] = Field(default_factory=list)
    start_hub: "Hub" = Field(default_factory=lambda: Hub())
    end_hub: "Hub" = Field(default_factory=lambda: Hub())
    connections_list: list["Connection"] = Field(default_factory=list)


class Hub(BaseModel):
    """Settings information for the hubs
    name
    """
    class MetaData(BaseModel):
        """Metadata for the hub
        """
        # TODO: Make an enum
        zone: str = Field(default="normal")
        # TODO: String to enum for colours
        colour: str = Field(default="None")
        max_drones: int = Field(default=maxsize)

    name: str = Field(default="")
    x: int = Field(default=(maxsize), gt=0)
    y: int = Field(default=maxsize, gt=0)
    meta_data: MetaData | None = Field(default_factory=MetaData)

    @model_validator(mode="after")
    def hub_validation(self) -> "Hub":
        for chr in self.name:
            if not chr.isprintable() or chr == " " or chr == "-":
                raise ParsingError(f"{self.name} is not a valid hub name")
        if self.meta_data:
            zone_set: set[str] = {
                "normal", "blocked", "restricted", "priority"}
            if self.meta_data.zone not in zone_set:
                raise ParsingError(
                    f"{self.name}.{self.meta_data.zone} is not a valid "
                    "zone name")
        return self


class Connection(BaseModel):
    """Settings information for the Connection
    """
    hubs_list: list[Hub] = Field(default_factory=list)
    max_link_capacity: int = Field(default=1, ge=0)


class InputError(Exception):
    def __init__(self, msg: str) -> None:
        """Error message specific to user input

        Args:
            msg (str): The message to display
        """
        super().__init__(f"Input Error: {msg}")


class ParsingError(Exception):
    def __init__(self, msg: str) -> None:
        """Error message specific to Parsing

        Args:
            msg (str): The message to display
        """
        super().__init__(f"Parsing Error: {msg}")
