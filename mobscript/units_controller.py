import json
import pathlib
from typing import Any, Dict, List, Tuple, Union

from .util.file_operations import load_json_from_file
from .util.file_operations import create_blank_file
from .data_structures.unit import Unit
from .data_structures.group import Group


class UnitsController:
    units_created_count = 0
    groups_created_count = 0
    units_data: Dict[str, Unit] = {}
    unit_types_data: Dict[int, Dict[str, Any]] = {}
    groups: Dict[str, Group] = {}

    def __init__(self, unit_types_file: pathlib.Path) -> None:
        self.unit_types_data = load_json_from_file(pathlib.Path(unit_types_file))

    def get_next_unit_key(self) -> str:
        self.units_created_count += 1
        return "unit_{}".format(self.units_created_count)

    def get_next_group_key(self) -> str:
        self.groups_created_count += 1
        return "group_{}".format(self.groups_created_count)

    def get_units_data(self) -> Dict[str, Unit]:
        return self.units_data

    def get_starting_positions(self) -> Dict[str, Tuple[Union[int, float], Union[int, float]]]:
        starting_positions = {}
        for key, value in self.units_data.items():
            starting_positions[key] = value.starting_position
        return starting_positions

    def get_waypoints(self) -> Dict[str, List[Tuple[Union[int, float], Union[int, float]]]]:
        waypoints = {}
        for key, value in self.units_data.items():
            waypoints[key] = value.waypoints
        return waypoints

    def get_waypoints_timelines(self) -> List[Dict[str, Any]]:
        waypoints_timelines = {}
        for key, value in self.units_data.items():
            waypoints_timelines[key] = value.waypoints_timeline
        return waypoints_timelines

    def save_generated_data(self, file_name: pathlib.Path) -> None:
        create_blank_file(file_name)
        combined_data = {
            "units": self.units_data,
            "groups": self.groups
        }
        pathlib.Path(file_name).write_text(
            json.dumps(combined_data, default=lambda o: o.encode(), indent=4)
        )

    def get_speed(self, key: str) -> Union[int, float]:
        return self.unit_types_data[self.units_data[key].unit_type]["speed"]

    def get_allowable_terrain(self, key: str) -> str:
        return self.unit_types_data[self.units_data[key].unit_type]["allowable_terrain"]

    def create_unit(self, 
                    name: str, 
                    unit_type: int, 
                    count=1, 
                    starting_position=(0, 0), 
                    waypoints=[], 
                    has_standard_radio=False,
                    has_cellular_radio=False, 
                    has_satellite_link=False) -> Dict[str, Unit]:
        units_created = []
        for _ in range(count):
            unit = Unit(
                self.get_next_unit_key(), 
                name, 
                unit_type, 
                starting_position, 
                waypoints, 
                has_standard_radio,
                has_cellular_radio,
                has_satellite_link
            )
            units_created.append(unit)
            self.units_data[unit.key] = unit
        return units_created

    def create_group(self, units: List[Unit]) -> Group:
        group = Group(self.get_next_group_key(), units)
        self.groups[group.key] = group
        return group

    def initialize_units(self) -> None:
        for key, value in self.units_data.items():
            value.initialize()

    def get_unit_keys(self) -> List[str]:
        return list(self.units_data.keys())