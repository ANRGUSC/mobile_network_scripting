


import pathlib
from typing import Any, Dict, Iterable, List, Tuple, Union
import importlib.util
import math
import contextlib
import os

from shapely.geometry.polygon import Polygon
from mobscript.data_structures.global_attributes import GlobalAttributes
from mobscript.data_structures.group import Group
from mobscript.data_structures.unit import Unit
from mobscript.delayed_instructions import DelayedInstructions
from mobscript.map_controller import MapController
from mobscript.units_controller import UnitsController
from mobscript.util.util import set_equipment

thisdir = pathlib.Path(__file__).resolve().parent


@contextlib.contextmanager
def cd(path):
    original_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)

class Instance:
    instance = None 
    script_count = 0

    def __init__(self) -> None:
        if Instance.instance is not None:
            raise RuntimeError(f"Instance has already been created")

        unit_types_file = thisdir.joinpath("input_data_defaults", "unit_types.json")
        map_file = thisdir.joinpath("input_data_defaults", "map.json")
        global_attributes_file = thisdir.joinpath("input_data_defaults", "global_attributes.json") 

        self.units_controller = UnitsController(unit_types_file)
        self.map_controller = MapController(map_file)
        self.global_attributes = GlobalAttributes(global_attributes_file)
        self.delayed_instructions = DelayedInstructions()

        Instance.instance = self 

    @staticmethod
    def get() -> "Instance":
        if Instance.instance is None:
            raise RuntimeError("Instance has not been created yet")
        return Instance.instance

    def load_script(self, path: pathlib.Path) -> None:
        with cd(path.parent):
            Instance.script_count += 1
            spec = importlib.util.spec_from_file_location(
                f"script_{Instance.script_count}",
                path
            )
            spec.loader.exec_module(importlib.util.module_from_spec(spec)) 

def create_units(unit_name: str, 
                 unit_type: int, 
                 unit_count: int,
                 starting_position=(0, 0), 
                 waypoints=[], 
                 has_standard_radio=False,
                 has_cellular_radio=False, 
                 has_satellite_link=False) -> Dict[str, Unit]:
    instance = Instance.get()
    return instance.units_controller.create_unit(
        unit_name, 
        unit_type, 
        unit_count,
        starting_position=(0, 0), 
        waypoints=[], 
        has_standard_radio=False,
        has_cellular_radio=False, 
        has_satellite_link=False
    )

def set_attribute(attribute: str, value: Any) -> None:
    instance = Instance.get()
    setattr(instance.global_attributes, attribute, value)

def equip(units_list: List[Unit], comm_type: str) -> None:
    comm_types = ["standard_radio", "cellular_radio", "satellite_link"]
    set_equipment(units_list, **{key: comm_type == key for key in comm_types})

def create_cellular_region(position_list: List[Tuple[int, int]]) -> None:
    instance = Instance.get()
    instance.map_controller.add_cellular_zone(Polygon(position_list))

def create_group(*unit_lists: Iterable[Unit]) -> Group:
    instance = Instance.get()
    flat_unit_list = [unit for unit_list in unit_lists for unit in unit_list]
    return instance.units_controller.create_group(flat_unit_list)

def set_starting_position(units_list: Iterable[Unit], 
                          starting_position: Tuple[int, int]) -> None:
    for unit in units_list:
        unit.starting_position = starting_position

def set_waypoints(units_list: Iterable[Unit], 
                  waypoints: Iterable[Tuple[int, int]],
                  start_time: int = 0,
                  end_time: int = math.inf) -> None:
    for unit in units_list:
        unit.waypoints_timeline.append({
            "waypoints": waypoints,
            "start_time": start_time,
            "end_time": end_time
        })

def load_map(file_name: Union[str, pathlib.Path]) -> None:
    instance = Instance.get()
    instance.map_controller.load_map(file_name)

def stop_movement(units_list: Iterable[Unit], stop_time: int) -> None:
    instance = Instance.get()
    instance.delayed_instructions.add_stop_movement(units_list, stop_time)

def change_equipment_at_time(units_list: Iterable[Unit], 
                             change_time: int,
                             turn_on: bool, 
                             equipment_name: str) -> None:
    instance = Instance.get()
    instance.delayed_instructions.add_change_equipment(
        [unit.key for unit in units_list], 
        change_time, turn_on, equipment_name=="standard_radio", 
        equipment_name=="cellular_radio", equipment_name=="satellite_link"
    )
