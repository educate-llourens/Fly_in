from colorama import Fore, Back
from src.classes import FlyInSettings


def basic_error_logging(msg: str) -> None:
    print(Fore.RED +
          f"{msg}\n" +
          Fore.RESET)


def log_title() -> None:
    print(Back.LIGHTBLUE_EX + Fore.WHITE +
          "--------------------------[ Fly-in ]---------------------------\n" +
          Back.RESET + Fore.RESET)


def log_heading(heading: str) -> None:
    print(Back.LIGHTCYAN_EX + Fore.WHITE +
          f"{heading}\n" +
          Back.RESET + Fore.RESET)


def log_start_information(settings: FlyInSettings) -> None:
    log_heading("Settings details")
    print(Fore.LIGHTCYAN_EX + "Number of drones: " + Fore.RESET +
          f"{settings.nbr_drones}")
    print("")
    for hub in settings.hubs_list:
        print(Fore.LIGHTCYAN_EX + "Hub: " + Fore.RESET,
              hub.name, hub.x, hub.y, "" + Fore.RESET, end="")
        if hub.meta_data:
            print(
                hub.meta_data.colour, hub.meta_data.max_drones,
                hub.meta_data.zone)
        else:
            print("")
    print("")
    for connection in settings.connections_list:
        print(Fore.LIGHTCYAN_EX + "Connection: " + Fore.RESET, end="")
        for hub in connection.hubs_list:
            print(hub.name, end=" ")
        if connection.max_link_capacity:
            print(Fore.LIGHTCYAN_EX + "| Max link capacity: " + Fore.RESET +
                  f"{connection.max_link_capacity}")
        else:
            print("")
    print("")
