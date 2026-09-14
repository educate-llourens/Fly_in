from colorama import Fore
from src.classes import FlyInSettings, InputError, ParsingError
from pydantic import ValidationError
from src.parsing import parsing
from sys import exit


def fly_in() -> None:
    try:
        settings: FlyInSettings = parsing()
        print_start_information(settings)
    except (InputError, ParsingError, ValidationError) as msg:
        print(Fore.RED + str(msg))
        exit(1)
    return


def print_start_information(settings: FlyInSettings) -> None:
    print(Fore.LIGHTCYAN_EX + "Number of drones: " + Fore.RESET +
          f"{settings.nbr_drones}")
    print("")
    for hub in settings.hubs_list:
        print(Fore.LIGHTCYAN_EX + "Hub: " + Fore.RESET,
              hub.name, hub.x, hub.y, hub.meta_data.colour,
              hub.meta_data.max_drones, hub.meta_data.zone, "" + Fore.RESET)
    print("")
    for connection in settings.connections_list:
        print(Fore.LIGHTCYAN_EX + "Connection: " + Fore.RESET, end="")
        for hub in connection.hubs_list:
            print(hub.name, end=" ")
        print(Fore.LIGHTCYAN_EX + "| Max link capacity: " + Fore.RESET +
              f"{connection.max_link_capacity}")
    print("")


if __name__ == "__main__":
    fly_in()
