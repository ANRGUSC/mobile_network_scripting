import json
from pathlib import Path


class Simulation:
    unit_data = {}
    simulation_data = {}

    def __init__(self, unit_data):
        self.unit_data = unit_data
        unit_file = Path("data/simulation.json")
        if unit_file.is_file() is False:
            with open("data/simulation.json", "w") as outfile:
                template = {}
                json.dump(template, outfile)

    def save_data(self):
        with open("data/simulation.json", "w") as outfile:
            json.dump(self.simulation_data, outfile, default=lambda o: o.encode(), indent=4)

    def calculate_paths(self):
        return self.unit_data.get_waypoints()

    def run_simulation(self, time_step, time_limit):
        calculated_paths = self.calculate_paths()
        current_positions = self.unit_data.get_starting_positions()
        print(current_positions)
        print(calculated_paths)
        self.simulation_data["positions"] = [
            {
                "test": 1
            },
            {
                "test": 2
            }
        ]
        self.simulation_data["positions"].append([
        ])
        print(time_step)
