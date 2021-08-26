import json
from pathlib import Path


class UnitsController:
    unit_data = {}
    unit_types_data = {}

    def __init__(self):
        with open("input_data/unit_types.json") as json_file:
            self.unit_types_data = json.load(json_file)

        unit_file = Path("generated_data/unit.json")
        if unit_file.is_file() is False:
            with open("generated_data/units.json", "w") as outfile:
                template = {}
                json.dump(template, outfile)

        with open('generated_data/units.json') as json_file:
            self.unit_data = json.load(json_file)

    def get_data(self):
        return self.unit_data

    def get_starting_positions(self):
        starting_positions = {}
        for key, value in self.unit_data.items():
            starting_positions[key] = value.starting_position
        return starting_positions

    def get_waypoints(self):
        waypoints = {}
        for key, value in self.unit_data.items():
            waypoints[key] = value.waypoints
        return waypoints

    def save_data(self):
        with open("generated_data/units.json", "w") as outfile:
            json.dump(self.unit_data, outfile, default=lambda o: o.encode(), indent=4)

    def get_speed(self, key):
        return self.unit_types_data[self.unit_data[key].unit_type]["speed"]

    def add_unit(self, unit):
        self.unit_data[unit.key] = unit
