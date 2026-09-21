from rich import print
from logging import getLogger
from rich.console import Console
from rich.logging import RichHandler
from src.settings import FlyInSettings


def basic_error_logging(msg: str) -> None:
    """Logs the error message to the console.

    Args:
        msg (str): The error message to log
    """
    console = Console()
    logger = getLogger("rich")
    logger.addHandler(RichHandler(console=console))
    logger.setLevel("ERROR")
    logger.error(msg)


def log_title() -> None:
    print(
          "[black on blue]"
          "------------------------[ Fly-in ]-------------------------"
          "[/black on blue]\n")


def log_heading(heading: str) -> None:
    print(f"[black on cyan] {heading} [/black on cyan]\n")


def log_start_information(settings: FlyInSettings) -> None:
    log_heading("Settings details")
    print("[cyan]Number of drones: [/cyan]"
          f"[default]{settings.nbr_drones}[/default]")
    print("")
    for hub in settings.hubs_list:
        print("[cyan]Hub: [/cyan] [default]"
              f"{hub.name} {hub.x} {hub.y}[/default]", end=" ")
        if hub.meta_data:
            print("[cyan] |[/cyan]", end=" ")
            print(
                f"[cyan]Colour:[/cyan] {hub.meta_data.colour}"
                "[cyan] Max drones:[/cyan] [default]"
                f"{hub.meta_data.max_drones}[/default]"
                f"[cyan] Zone:[/cyan] {hub.meta_data.hub_access_type}")
        else:
            print("")
    print("")
    for connection in settings.connections_list:
        print("[cyan]Connection: [/cyan]", end="")
        print(f"[default]{connection.connection_start_hub.name}[/default]",
              end=" ")
        print(f"[default]{connection.connection_end_hub.name}[/default]",
              end=" ")
        if connection.max_link_capacity:
            print("[cyan]| Max link capacity: [/cyan]"
                  f"[default]{connection.max_link_capacity}[/default]")
        else:
            print("")
    print("")
