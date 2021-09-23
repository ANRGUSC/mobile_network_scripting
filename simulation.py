import copy
import json
import math
from pathlib import Path
from util.file_operations import create_blank_file


class Simulation:
    units_controller = {}
    simulation_data = {}

    def __init__(self, units_controller, map_controller, delayed_instructions):
        self.units_controller = units_controller
        self.map_controller = map_controller
        self.delayed_instructions = delayed_instructions
        create_blank_file("generated_data", "simulation.json")

    def save_generated_data(self):
        with open("generated_data/simulation.json", "w") as outfile:
            json.dump(self.simulation_data, outfile, default=lambda o: o.encode(), indent=4)

    def calculate_coord_change_direction(self, current_coord, destination_coord):
        triangle_dist_x = abs(current_coord[0] - destination_coord[0])
        triangle_dist_y = abs(current_coord[1] - destination_coord[1])

        if triangle_dist_x == 0:
            return 0, 1
        elif triangle_dist_y == 0:
            return 1, 0

        ratio = triangle_dist_y / triangle_dist_x
        sum_of_squares = 1 + ratio * ratio
        common_denom = math.sqrt(1 / sum_of_squares)
        change_x = common_denom
        change_y = ratio * common_denom
        return (change_x if current_coord[0] < destination_coord[0] else -change_x, 
                change_y if current_coord[1] < destination_coord[1] else -change_y)

    def calculate_dist_between_points(self, point_1, point_2):
        return math.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

    def clamp_new_coord(self, current_coord, destination_coord, unclamped_new_coord, dist_to_unclamped):
        dist_to_destination = self.calculate_dist_between_points(current_coord, destination_coord)
        if dist_to_unclamped > dist_to_destination:
            return destination_coord
        return unclamped_new_coord

    def move_given_path(self, unit_key, current_coord, current_path, time_left):
        coord_change_direction = None
        while time_left > 0 and len(current_path) > 0:
            destination_coord = current_path[0]
            if coord_change_direction is None:
                coord_change_direction = self.calculate_coord_change_direction(current_coord, destination_coord)
            coord_change_scaled = ([self.units_controller.get_speed(unit_key) * time_left * value for value in coord_change_direction])
            unclamped_new_coord = (current_coord[0] + coord_change_scaled[0], current_coord[1] + coord_change_scaled[1])
            dist_to_unclamped = self.calculate_dist_between_points(current_coord, unclamped_new_coord)
            clamped_new_coord = self.clamp_new_coord(current_coord, destination_coord, unclamped_new_coord, dist_to_unclamped)
            dist_to_clamped = self.calculate_dist_between_points(current_coord, clamped_new_coord)    
            time_left *= (1 - (dist_to_clamped / dist_to_unclamped))
            if clamped_new_coord == destination_coord:
                current_path.pop(0)
                coord_change_direction = None
            current_coord = clamped_new_coord
        return current_coord

    def run_simulation(self, time_step, time_limit):
        current_positions = self.units_controller.get_starting_positions()
        waypoints_timelines = self.units_controller.get_waypoints_timelines()
        unit_to_end_time = {}
        current_paths = {}
        for unit_key in self.units_controller.get_unit_keys():
            unit_to_end_time[unit_key] = math.inf
            current_paths[unit_key] = []

        current_time = 0
        positions_history = []
        self.simulation_data["metadata"] = {
            "time_step": time_step,
            "time_limit": time_limit
        }
        self.simulation_data["positions"] = []
        while current_time <= time_limit:
            for unit_key, current_coord in current_positions.items():
                waypoints_timeline = waypoints_timelines[unit_key]
                if len(waypoints_timeline) >= 1 and waypoints_timeline[0]["start_time"] <= current_time:
                    waypoints_to_follow = waypoints_timeline[0]["waypoints"]
                    unit_to_end_time[unit_key] = waypoints_timeline[0]["end_time"]
                    current_paths[unit_key] = self.map_controller.convert_waypoints_to_path(waypoints_to_follow, self.units_controller.get_allowable_terrain(unit_key))
                    waypoints_timeline.pop(0)
                if self.delayed_instructions.get_stop_movement_time(unit_key) <= current_time:
                    current_paths[unit_key] = []
                    self.delayed_instructions.remove_stop_movement_time(unit_key)
                if unit_to_end_time[unit_key] <= current_time:
                    current_paths[unit_key] = []
                new_coord = self.move_given_path(unit_key, current_coord, current_paths[unit_key], time_step)
                current_positions[unit_key] = new_coord
            current_time += time_step
            positions_history.append(copy.deepcopy(current_positions))
            self.simulation_data["positions"].append([
                copy.deepcopy(current_positions)
            ])
        return positions_history
