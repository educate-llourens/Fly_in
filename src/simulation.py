from src.settings import FlyInSettings, Connection, Drone
from src.project_logging import (basic_error_logging, log_key_value,
                                 log_move_info)
from rich import print
from src.settings import Hub, HubAccessType
from src.pathfinding import Pathfinding


class SimulationEngine:
    nbr_turns: int = 0

    def __init__(self, settings: FlyInSettings) -> None:
        """Initiates the simulation

        Args:
            settings (FlyInSettings): settings for the simulation
        """
        self.settings: FlyInSettings = settings
        self.graph: dict[str, list[Connection]] = self.create_graph()
        self.drones_list: list[Drone] = settings.drones_list
        self.pathfinder: Pathfinding = Pathfinding()

        for hub in settings.hubs_list:
            hub.hub_rules()

    def create_graph(self) -> dict[str, list[Connection]]:
        """Creates an adjacency map

        Returns:
            dict[str, list[Connection]]: A dictionary of the nodes and their
            connections
        """
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

    def run(self) -> None:
        """Runs the simulation from start to end
        """
        end_hub = self.settings.end_hub
        turn = 0

        self.assign_drone_path()
        while (
            len(
                [
                    drone
                    for drone in self.drones_list
                    if drone.current_hub.name != end_hub.name
                ]) > 0
        ):
            turn += 1
            log_key_value("Turn", str(turn))
            self.move_drones()

    def assign_drone_path(self) -> None:
        """Assigns each drone their path and increases the cost of the path
        everytime a drone chooses that path
        """
        drones_list = self.settings.drones_list
        for drone in drones_list:
            drone.path = self.pathfinder.dijkstra(
                self.settings.start_hub.name, self.settings.end_hub.name,
                self.graph)
            middle = drone.path[1:-1]
            for hub in self.settings.hubs_list:
                if hub.name in middle:
                    hub.hub_cost += 5

    def move_drones(self) -> None:
        """Moves the drones each turn
        """
        def handle_restricted() -> None:
            """Handles the resttricted hub during movement
            """
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

        def find_connection(start_name: str,
                            end_name: str) -> Connection | None:
            """Finds the connection to move on

            Args:
                start_name (str): Start the movement from this hub
                end_name (str): End the movement on this hub

            Returns:
                Connection | None: The connection tomove on or none
            """
            for connection in self.graph[start_name]:
                names: set[str] = {connection.connection_start_hub.name,
                                   connection.connection_end_hub.name}
                if names == {start_name, end_name}:
                    return connection
            return None

        drones_list = self.settings.drones_list
        end_name: str = self.settings.end_hub.name
        connection_capacity: int = 0

        for drone in drones_list:
            current_name: str = drone.current_hub.name
            if current_name == end_name:
                continue
            # Find next hub and connection ------------------------------------
            next_name: str = drone.path[drone.path.index(current_name) + 1]
            found_connection: Connection | None = find_connection(
                current_name, next_name)
            if found_connection is None:
                continue
            connection = found_connection
            connection_capacity = connection.max_link_capacity
            next_end_hub: Hub = (
                connection.connection_end_hub
                if connection.connection_end_hub.name == next_name
                else connection.connection_start_hub
            )
            # Handle rules ----------------------------------------------------
            if next_end_hub.nbr_hub_drones < next_end_hub.meta_data.max_drones:
                if drone.current_hub.nbr_hub_drones > 0:
                    drone.current_hub.nbr_hub_drones -= 1
                if next_end_hub.meta_data.hub_access_type == (
                        HubAccessType.restricted):
                    handle_restricted()
            # Move drone ------------------------------------------------------
                else:
                    drone.current_hub = next_end_hub
                    if drone in connection.que:
                        connection.que.remove(drone)
                drone.current_hub.nbr_hub_drones += 1
            # Log the movement for the drone ----------------------------------
            log_move_info(
                drone.id,
                current_name,
                drone.current_hub.name,
                drone.current_hub.nbr_hub_drones,
                drone.current_hub.meta_data.max_drones,
                connection_capacity,
                connection.que
            )
        print("")
