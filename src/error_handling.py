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


class SimulationError(Exception):
    def __init__(self, msg: str) -> None:
        """Error message specific to Simulation

        Args:
            msg (str): The message to display
        """
        super().__init__(f"Simulation Error: {msg}")
