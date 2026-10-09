from rich import print
from logging import getLogger
from rich.console import Console
from rich.logging import RichHandler
from src.settings import FlyInSettings, Drone


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
    """Logs the program title with correct formatting
    """
    print(
        "[black on blue]"
        "------------------------[ Fly-in ]-------------------------"
        "[/black on blue]\n"
    )


def log_heading(heading: str) -> None:
    """Logs a heading with the correct formatting

    Args:
        heading (str): The message to display
    """
    print(f"[black on cyan] {heading} [/black on cyan]\n")


def log_start_information(settings: FlyInSettings) -> None:
    """Logs the start information once the file has been
    processed.

    Args:
        settings (FlyInSettings): The settings class to retrieve
        the information we want to display.
    """
    log_heading("Settings details")
    print("")
    for hub in settings.hubs_list:
        print(
            "[cyan]Hub: [/cyan] [default]"
            f"{hub.name} {hub.x} {hub.y}[/default]",
            end=" ",
        )
        if hub.meta_data:
            print("[cyan] |[/cyan]", end=" ")
            print(
                f"[cyan]Colour:[/cyan] {hub.meta_data.colour}"
                "[cyan] Max drones:[/cyan] [default]"
                f"{hub.meta_data.max_drones}[/default]"
                f"[cyan] Zone:[/cyan] {hub.meta_data.hub_access_type}"
            )
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
            print(
                "[cyan]| Max link capacity: [/cyan]"
                f"[default]{connection.max_link_capacity}[/default]"
            )
        else:
            print("")
    print("")


def log_drone_creation(settings: FlyInSettings) -> None:
    """Logs the drones created

    Args:
        settings (FlyInSettings): Class we are retrieving the
        information from.
    """
    for drone in settings.drones_list:
        print("[cyan]Created drone with id: [/cyan]"
              f"[default]{drone.id}[/default]")
    print("")
    log_key_value("Number of drones created", str(settings.nbr_drones))
    print("")


def log_information(msg: str) -> None:
    """Logs information with the correct formatting

    Args:
        msg (str): Message to display
    """
    print(f"[cyan]{msg}[/cyan]\n")


def log_key_value(key: str, value: str) -> None:
    """Logs key value pairs with correct formatting

    Args:
        key (str): Key to display
        value (str): Value to display
    """
    print(f"[cyan]{key}: [/cyan][default]{value}[/default]")


def log_move_info(
    drone_id: int,
    start_hub: str,
    end_hub: str,
    nbr_drones_at_destination: int,
    max_drones_at_destination: int,
    connection_max_drones: int,
    que: list[Drone],
) -> None:
    """Logs the movement of the drones across the map

    Args:
        drone_id (int): id of the moving drone
        start_hub (str): Hub where it started
        end_hub (str): Hub where it ended
        nbr_drones_at_destination (int): Number of drones already at the
        destination hub
        max_drones_at_destination (int): The maximum number of drones allowed
        at the destination hub
        connection_max_drones (int): Maximum number of drones allowed on
        the connection
        que (list[Drone]): Que of drones waiting on the connection
    """
    len_connection_que: int = len(que)
    print(
        f"[cyan]{drone_id}[/cyan]:"
        f"[default]{start_hub} -> {end_hub} [/default]"
        "[cyan]| Hub drones: [/cyan]"
        f"[default]{nbr_drones_at_destination}/"
        f"{max_drones_at_destination}[/default]"
        "[cyan] | Connection drones: [/cyan]"
        f"[default]{len_connection_que}/"
        f"{connection_max_drones}[/default]",
        end=" ",
    )
    drone_ids: list[int] = [drone.id for drone in que]
    if drone_id in drone_ids:
        print(
            "[yellow][On connection] "
            f"[Turn={
                [
                    drone.on_connection_turn
                    for drone in que
                    if drone.id == drone_id
                ][0]}][/yellow]"
        )
    elif start_hub == end_hub and drone_id not in drone_ids:
        print(f"[yellow][Waiting at {start_hub}][/yellow]")
    else:
        print("")
