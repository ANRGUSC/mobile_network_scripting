import json
from pathlib import Path


class UnitData:
    unit_data = {}

    def __init__(self):
        unit_file = Path("data/unit.json")
        if unit_file.is_file() is False:
            with open("data/units.json", "w") as outfile:
                template = {}
                json.dump(template, outfile)

        with open('data/units.json') as json_file:
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
        with open("data/units.json", "w") as outfile:
            json.dump(self.unit_data, outfile, default=lambda o: o.encode(), indent=4)

    def add_unit(self, unit):
        self.unit_data[unit.key] = unit
