import json
from pathlib import Path
from util.file_operations import load_json_from_file
from util.file_operations import create_blank_file

class UnitsController:
    units_data = {}
    unit_types_data = {}

    def __init__(self):
        self.unit_types_data = load_json_from_file("input_data", "unit_types.json")
        create_blank_file("generated_data", "units.json")

    def get_units_data(self):
        return self.units_data

    def get_starting_positions(self):
        starting_positions = {}
        for key, value in self.units_data.items():
            starting_positions[key] = value.starting_position
        return starting_positions

    def get_waypoints(self):
        waypoints = {}
        for key, value in self.units_data.items():
            waypoints[key] = value.waypoints
        return waypoints

    def save_data(self):
        with open("generated_data/units.json", "w") as outfile:
            json.dump(self.units_data, outfile, default=lambda o: o.encode(), indent=4)

    def get_speed(self, key):
        return self.unit_types_data[self.units_data[key].unit_type]["speed"]

    def add_unit(self, unit):
        self.units_data[unit.key] = unit
