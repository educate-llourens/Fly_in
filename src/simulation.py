from src.settings import FlyInSettings, Connection
from src.project_logging import (basic_error_logging, log_key_value,
                                 log_move_info)
from rich import print


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
        end_hub = self.settings.end_hub
        drones_list = self.settings.drones_list
        graph = self.graph
        turn: int = 0

        while (len([drone
                    for drone in drones_list
                    if drone.current_hub.name != end_hub.name
                    ]) > 0 and turn < 10):
            turn += 1
            log_key_value("Turn", str(turn))
            for drone in drones_list:
                start_hub: str = drone.current_hub.name
                for connection in graph[drone.current_hub.name]:
                    if (
                        connection.connection_start_hub.name
                            == drone.current_hub.name):
                        next_connection: Connection = connection
                        drone.current_hub = next_connection.connection_end_hub
                        drone.current_hub.nbr_hub_drones += 1
                log_move_info(drone.id, start_hub, drone.current_hub.name,
                              drone.current_hub.nbr_hub_drones,
                              drone.current_hub.meta_data.max_drones)
            print("")
