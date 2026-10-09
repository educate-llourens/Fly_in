from src.settings import Connection, Hub, HubAccessType
from heapq import heappop, heappush


class Pathfinding:
    def dijkstra(self, start_name: str, goal_name: str,
                 graph: dict[str, list[Connection]]) -> list[str]:
        """Dijkstra pathfinding algorithm

        Args:
            start_name (str): Start hub name
            goal_name (str): Goal hub name
            graph (dict[str, list[Connection]]): Adjacency map

        Returns:
            list[str]: list of hub names as the path
        """
        cost: dict[str, int] = {start_name: 0}
        previous: dict[str, str] = {}
        working_list: list[tuple[int, str]] = [(0, start_name)]
        visited: set = set()

        while working_list:
            current_cost, current_name = heappop(working_list)
            if current_name in visited:
                continue
            visited.add(current_name)
            if current_name == goal_name:
                break
            for connection in graph[current_name]:
                next_hub: Hub = connection.connection_end_hub
                if next_hub.meta_data.hub_access_type == HubAccessType.blocked:
                    continue
                if next_hub.name in visited:
                    continue
                new_cost: int = current_cost + next_hub.hub_cost
                if new_cost < cost.get(next_hub.name, float('inf')):
                    cost[next_hub.name] = new_cost
                    previous[next_hub.name] = current_name
                    heappush(working_list, (new_cost, next_hub.name))
        path: list[str] = [goal_name]
        while path[-1] != start_name:
            path.append(previous[path[-1]])
        path.reverse()
        return path
