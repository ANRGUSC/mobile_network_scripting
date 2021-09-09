import copy
import json
import math
from pathlib import Path
from util.file_operations import create_blank_file

def calculate_new_coord(current_coord, destination_coord, coord_change):
    if current_coord[0] < destination_coord[0]:
        new_x = current_coord[0] + coord_change[0]
        if new_x > destination_coord[0]:
            new_x = destination_coord[0]
    else:
        new_x = current_coord[0] - coord_change[0]
        if new_x < destination_coord[0]:
            new_x = destination_coord[0]
    if current_coord[1] < destination_coord[1]:
        new_y = current_coord[1] + coord_change[1]
        if new_y > destination_coord[1]:
            new_y = destination_coord[1]
    else:
        new_y = current_coord[1] - coord_change[1]
        if new_y < destination_coord[1]:
            new_y = destination_coord[1]
    return new_x, new_y

def calculate_coord_change_direction(time_step, current_coord, destination_coord):
    triangle_dist_x = abs(current_coord[0] - destination_coord[0])
    triangle_dist_y = abs(current_coord[1] - destination_coord[1])

    if triangle_dist_x == 0:
        return 0, time_step
    elif triangle_dist_y == 0:
        return time_step, 0

    ratio = triangle_dist_y / triangle_dist_x
    sum_of_squares = 1 + ratio * ratio
    common_denom = math.sqrt(1 / sum_of_squares)
    change_x = time_step * common_denom
    change_y = time_step * ratio * common_denom
    return change_x, change_y

class Simulation:
    units_controller = {}
    simulation_data = {}
    simulation_file = None

    def __init__(self, units_controller):
        self.units_controller = units_controller
        self.simulation_file = create_blank_file("generated_data", "simulation.json")

    def save_data(self):
        with open("generated_data/simulation.json", "w") as outfile:
            json.dump(self.simulation_data, outfile, default=lambda o: o.encode(), indent=4)

    def calculate_paths(self):
        return self.units_controller.get_waypoints()

    def move_given_path(self, unit_key, current_coord, current_path, time_step):
        if len(current_path) == 0:
            return
        destination_coord = current_path[0]
        coord_change_direction = calculate_coord_change_direction(time_step, current_coord, destination_coord)
        coord_change_scaled = ([self.units_controller.get_speed(unit_key) * value for value in coord_change_direction])
        new_coord = calculate_new_coord(current_coord, destination_coord, coord_change_scaled)
        if new_coord == destination_coord:
            current_path.pop(0)
        return new_coord

    def run_simulation(self, time_step, time_limit):
        current_paths = self.calculate_paths()
        current_positions = self.units_controller.get_starting_positions()
        current_time = 0
        positions_history = []
        self.simulation_data["metadata"] = {
            "time_step": time_step,
            "time_limit": time_limit
        }
        self.simulation_data["positions"] = []
        while current_time <= time_limit:
            for unit_key, current_coord in current_positions.items():
                new_coord = self.move_given_path(unit_key, current_coord, current_paths[unit_key], time_step)
                current_positions[unit_key] = new_coord
            current_time += time_step
            positions_history.append(copy.deepcopy(current_positions))
            self.simulation_data["positions"].append([
                copy.deepcopy(current_positions)
            ])
        return positions_history
