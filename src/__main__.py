from src.project_logging import (
    basic_error_logging, log_title, log_start_information)
from pydantic import ValidationError
from argparse import ArgumentParser, Namespace
from sys import exit, argv
from pathlib import Path
from src.settings import FlyInSettings
from src.error_handling import InputError, ParsingError
from src.parsing import Parser
from src.simulation import SimulationEngine


def fly_in() -> None:
    # Parsing -----------------------------------------------------------------
    if len(argv) > 2:
        raise InputError("The program only takes the config file as "
                         "an argument")
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "map",
        default="maps/01_linear_path.txt"
    )
    args: Namespace = arg_parser.parse_args()
    path_map = str(Path(args.map))
    parser: Parser = Parser(path_map)
    try:
        settings: FlyInSettings = parser.parse_file()
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

    # Simulation --------------------------------------------------------------
    simulation: SimulationEngine = SimulationEngine(settings)
    return


if __name__ == "__main__":
    fly_in()
