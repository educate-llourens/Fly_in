from src.logging import (log_start_information, basic_error_logging,
                         log_title)
from src.classes import FlyInSettings, InputError, ParsingError
from pydantic import ValidationError
from src.parsing import parsing
from sys import exit


def fly_in() -> None:
    try:
        settings: FlyInSettings = parsing()
    except (InputError, ParsingError, ValidationError) as msg:
        basic_error_logging(str(msg))
        exit(1)
    log_title()
    log_start_information(settings)
    return


if __name__ == "__main__":
    fly_in()
