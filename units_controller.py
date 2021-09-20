import json
from pathlib import Path
from util.file_operations import load_json_from_file
from util.file_operations import create_blank_file
from data_structures.unit import Unit
from data_structures.group import Group


class UnitsController:
    units_created_count = 0
    groups_created_count = 0
    units_data = {}
    unit_types_data = {}
    groups = {}

    def __init__(self):
        self.unit_types_data = load_json_from_file("input_data/unit_types.json")
        create_blank_file("generated_data", "units.json")

    def get_next_unit_key(self):
        self.units_created_count += 1
        return "unit_{}".format(self.units_created_count)

    def get_next_group_key(self):
        self.groups_created_count += 1
        return "group_{}".format(self.groups_created_count)

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

    def get_waypoints_timelines(self):
        waypoints_timelines = {}
        for key, value in self.units_data.items():
            waypoints_timelines[key] = value.waypoints_timeline
        return waypoints_timelines

    def save_generated_data(self):
        with open("generated_data/units.json", "w") as outfile:
            combined_data = {
                "units": self.units_data,
                "groups": self.groups
            }
            json.dump(combined_data, outfile, default=lambda o: o.encode(), indent=4)

    def get_speed(self, key):
        return self.unit_types_data[self.units_data[key].unit_type]["speed"]

    def create_unit(self, name, unit_type, count=1, starting_position=(0, 0), waypoints=[], has_standard_radio=False,
                    has_cellular_radio=False, has_satellite_link=False):
        units_created = []
        for i in range(count):
            unit = Unit(self.get_next_unit_key(), name, unit_type, starting_position, waypoints, has_standard_radio,
                        has_cellular_radio,
                        has_satellite_link)
            units_created.append(unit)
            self.units_data[unit.key] = unit
        return units_created

    def create_group(self, units):
        group = Group(self.get_next_group_key(), units)
        self.groups[group.key] = group
        return group

    def initialize_units(self):
        for key, value in self.units_data.items():
            value.initialize()

    def get_unit_keys(self):
        return list(self.units_data.keys())