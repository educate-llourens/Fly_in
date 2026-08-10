from colorama import Fore


def fly_in() -> None:
    try:
        settings: FlyInSettings = FlyInSettings()
    except (FileExistsError, FileNotFoundError, ValueError) as msg:
        print(Fore.RED + str(msg))
    return


if __name__ == "__main__":
    fly_in()
