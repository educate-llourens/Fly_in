from src.project_logging import (
    basic_error_logging, log_title, log_start_information)
from src.classes import FlyInSettings, InputError, ParsingError
from pydantic import ValidationError
from src.parsing import parsing
from sys import exit


def fly_in() -> None:
    # Parsing -----------------------------------------------------------------
    try:
        settings: FlyInSettings = parsing()
    except (InputError, ParsingError, ValidationError) as error:
        if isinstance(error, ValidationError):
            for msg in error.errors():
                basic_error_logging(
                    f"{msg['msg']} for {msg['loc']} = {msg['input']}")
        else:
            basic_error_logging(str(error))
        exit(1)
    log_title()
    log_start_information(settings)

    # -------------------------------------------------------------------------

    return


if __name__ == "__main__":
    fly_in()
