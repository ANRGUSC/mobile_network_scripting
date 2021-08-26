import json
import math
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

    @staticmethod
    def calculate_coord_change(current_coord, destination_coord):
        triangle_dist_x = abs(current_coord[0] - destination_coord[0])
        triangle_dist_y = abs(current_coord[1] - destination_coord[1])
        ratio = triangle_dist_y / triangle_dist_x
        sum_of_squares = 1 + ratio * ratio
        common_denom = math.sqrt(1 / sum_of_squares)
        change_x = common_denom
        change_y = ratio * common_denom
        return change_x, change_y

    def run_simulation(self, time_step, time_limit):
        calculated_paths = self.calculate_paths()
        current_positions = self.unit_data.get_starting_positions()
        current_time = 0
        while current_time <= time_limit:
            print(current_positions)
            for key, current_coord in current_positions.items():
                destination_coord = calculated_paths[key][0]
                coord_change = self.calculate_coord_change(current_coord, destination_coord)

                if current_coord[0] < destination_coord[0]:
                    new_x = current_coord[0] + coord_change[0]
                else:
                    new_x = current_coord[0] - coord_change[0]
                if current_coord[1] < destination_coord[1]:
                    new_y = current_coord[1] + coord_change[1]
                else:
                    new_y = current_coord[1] - coord_change[1]
                current_positions[key] = (new_x, new_y)
            current_time += time_step

        self.simulation_data["positions"] = []
        self.simulation_data["positions"].append([
            {
                "test": 1
            },
            {
                "test": 2
            }
        ])
        #print(time_step)
