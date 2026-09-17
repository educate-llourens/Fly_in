from src.error_handling import SimulationError
from src.settings import FlyInSettings, Drone


class SimulationEngine:
    drones_list: list[Drone] = []

    def __init__(self, settings: FlyInSettings) -> None:
        self.settings = settings

        for i in range(self.settings.nbr_drones - 1):
            self.drones_list.append(Drone(i + 1))
