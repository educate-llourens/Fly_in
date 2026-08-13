from colorama import Fore
from src.classes import FlyInSettings, InputError
from src.parsing import parsing


def fly_in() -> None:
    try:
        settings: FlyInSettings = parsing()
    except (FileExistsError, FileNotFoundError, ValueError, InputError) as msg:
        print(Fore.RED + str(msg))
    return settings


if __name__ == "__main__":
    fly_in()
