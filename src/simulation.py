from src.settings import FlyInSettings, Connection, Drone
from src.project_logging import (basic_error_logging, log_key_value,
                                 log_move_info)
from rich import print
from src.settings import Hub, HubAccessType


class SimulationEngine:
    nbr_turns: int = 0

    def __init__(self, settings: FlyInSettings) -> None:
        self.settings: FlyInSettings = settings
        self.graph: dict[str, list[Connection]] = self.create_graph()

        for hub in settings.hubs_list:
            hub.hub_rules()

    def create_graph(self) -> dict[str, list[Connection]]:
        graph_dict: dict[str, list[Connection]] = {}
        for connection in self.settings.connections_list:
            start_name = connection.connection_start_hub.name
            end_name = connection.connection_end_hub.name
            if start_name not in graph_dict:
                graph_dict[start_name] = []
            graph_dict[start_name].append(connection)
            if end_name not in graph_dict:
                graph_dict[end_name] = []
            graph_dict[end_name].append(connection)
        return graph_dict

    def move_drones(self) -> None:
        def handle_restricted():
            if (drone not in connection.que and
                    len(connection.que) < connection.max_link_capacity):
                connection.que.append(drone)
            drone.on_connection_turn += 1
            if drone.on_connection_turn > 1:
                if (next_end_hub.nbr_hub_drones <
                        next_end_hub.meta_data.max_drones):
                    drone.current_hub = next_end_hub
                    connection.que.remove(drone)
                else:
                    basic_error_logging(f"Drone {drone.id} is stuck on "
                                        "connection starting at "
                                        f"{drone.current_hub.name}")

        end_hub = self.settings.end_hub
        drones_list = self.settings.drones_list
        graph = self.graph
        turn: int = 0
        connection_capacity: int = 0
        log_que: list[Drone] = []

        while (
            len(
                [
                    drone
                    for drone in drones_list
                    if drone.current_hub.name != end_hub.name
                ]) > 0 and turn < 10
        ):
            turn += 1
            log_key_value("Turn", str(turn))
            for drone in drones_list:
                start_hub_name: str = drone.current_hub.name
                for connection in graph[drone.current_hub.name]:
                    connection_capacity = connection.max_link_capacity
                    start_hub: Hub = connection.connection_start_hub
                    end_hub: Hub = connection.connection_end_hub
                    next_connection: Connection = connection
                    next_end_hub: Hub = next_connection.connection_end_hub

                    if (start_hub.name == drone.current_hub.name):
                        if (
                            next_end_hub.meta_data.max_drones
                            > next_end_hub.nbr_hub_drones
                        ):
                            if drone.current_hub.nbr_hub_drones > 0:
                                drone.current_hub.nbr_hub_drones -= 1
                            if next_end_hub.meta_data.hub_access_type == (
                                    HubAccessType.restricted):
                                handle_restricted()
                            else:
                                drone.current_hub = next_end_hub
                                if drone in connection.que:
                                    connection.que.remove(drone)
                            drone.current_hub.nbr_hub_drones += 1
                    log_que = connection.que
                log_move_info(
                    drone.id,
                    start_hub_name,
                    drone.current_hub.name,
                    drone.current_hub.nbr_hub_drones,
                    drone.current_hub.meta_data.max_drones,
                    connection_capacity,
                    log_que
                )
            print("")
