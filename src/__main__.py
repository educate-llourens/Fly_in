from colorama import Fore
from classes import FlyInSettings, InputError
from parsing import parsing
from enum import Enum


def fly_in() -> None:
    try:
        settings: FlyInSettings = parsing()
        if not settings:
            print(Fore.RED + "Parsing Error: Settings is empty" + Fore.RESET)
        print_start_information(settings)
    except (FileExistsError, FileNotFoundError, ValueError, InputError) as msg:
        print(Fore.RED + str(msg))
    return


def print_start_information(settings: FlyInSettings) -> None:
    print(Fore.LIGHTCYAN_EX + "Number of drones: " + Fore.RESET +
          f"{settings.nbr_drones}")
    print("")
    print(Fore.LIGHTCYAN_EX + "Start hub: " + Fore.RESET,
          settings.start_hub.name + Fore.RESET,
          settings.start_hub.x, settings.start_hub.y,
          settings.start_hub.meta_data.colour,
          settings.start_hub.meta_data.max_drones,
          settings.start_hub.meta_data.zone)
    for hub in settings.hubs_list:
        print(Fore.LIGHTCYAN_EX + "Hub: " + Fore.RESET,
              hub.name, hub.x, hub.y, hub.meta_data.colour,
              hub.meta_data.max_drones, hub.meta_data.zone + Fore.RESET)
    print(Fore.LIGHTCYAN_EX + "End hub: " + Fore.RESET,
          settings.end_hub.name, settings.end_hub.x,
          settings.end_hub.y, settings.end_hub.meta_data.colour,
          settings.end_hub.meta_data.max_drones,
          settings.end_hub.meta_data.zone)
    print("")
    for connection in settings.connections_list:
        print(Fore.LIGHTCYAN_EX + "Connection: ",
              connection.connections)


if __name__ == "__main__":
    fly_in()
