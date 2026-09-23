from src.settings import FlyInSettings, Connection, Hub, HubAccessType
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

    def run_simulation(self) -> None:
        settings = self.settings
        # start_hub = self.settings.start_hub
        end_hub = self.settings.end_hub
        drones_list = self.settings.drones_list
        graph = self.graph

        while end_hub.nbr_hub_drones < settings.nbr_drones:
            self.nbr_turns += 1
            for drone in drones_list:
                next_hub: Hub = (
                    graph[drone.current_hub_name][0].connection_end_hub)
                if self.can_move(next_hub):
                    drone.current_hub_name = next_hub.name
                    next_hub.nbr_hub_drones += 1
                else:
                    continue
        print(
            f"[cyan]Drone {drone.id}:[/cyan] "
            f"[default]{drone.current_hub_name}[/default]")

    def can_move(self, next_hub: Hub) -> bool:
        if next_hub.meta_data.hub_access_type != HubAccessType.blocked:
            if (next_hub.nbr_hub_drones < next_hub.meta_data.max_drones):
                return True
        return False
