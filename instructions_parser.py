import graph_analyzer
from units_controller import *
from simulation import Simulation
from shapely.geometry.polygon import Polygon
from data_structures.instruction_line import InstructionLine
import re
from util.util import set_starting_positions, set_equipment, split_list_with_braces, set_waypoints


def convert_to_units_list(value, var_to_units, var_to_group):
    split = list(filter(None, re.split(r'\[|\]', value)))
    var_name = split[0]
    if var_name in var_to_units:
        units_list = var_to_units[var_name]
    elif var_name in var_to_group:
        units_list = var_to_group[var_name].units_list
    if len(split) == 1:
        return units_list
    index_range = split[1].split(":")
    return units_list[int(index_range[0]):int(index_range[1])]


def generate_position(value, var_to_position):
    if value in var_to_position:
        return var_to_position[value]
    split = list(filter(None, re.split(r'\(|\)|,', value)))
    return float(split[0]), float(split[1])


def generate_position_list(value, var_to_position):
    if value in var_to_position:
        return var_to_position[value]
    value = value[1:len(value) - 1]
    position_tuple_list = []
    for position_string in split_list_with_braces(value):
        position_tuple_list.append(generate_position(position_string, var_to_position))
    return position_tuple_list


def remove_quotes(value):
    return value.replace("\"", "")


class InstructionsParser:
    var_to_units = {}
    var_to_group = {}
    var_to_position = {}
    cellular_zones = []

    time_duration = None
    time_step = None

    def __init__(self, units_controller):
        self.units_controller = units_controller

    def parse_file(self, file_name):
        with open(file_name) as instructions_file:
            for line in instructions_file:
                if not line.strip():
                    continue
                instruction_line = InstructionLine(line)
                initialized_variable = instruction_line.initialized_variable
                function_name = instruction_line.function_name
                param_list = instruction_line.param_list

                # delete
                print(initialized_variable, function_name, param_list, flush=True)
                # delete

                if function_name == "create_units":
                    unit_name = remove_quotes(param_list[0])
                    unit_type = remove_quotes(param_list[1])
                    unit_count = int(param_list[2])
                    units_created = self.units_controller.create_unit(unit_name, unit_type, unit_count)
                    self.var_to_units[initialized_variable] = units_created
                elif function_name == "set_time":
                    attribute = remove_quotes(param_list[0])
                    if attribute == "duration":
                        time_duration = float(param_list[1])
                    elif attribute == "step":
                        time_step = float(param_list[1])
                elif function_name == "equip":
                    units_list = convert_to_units_list(param_list[0], self.var_to_units, self.var_to_group)
                    if param_list[1] == "standard_radio":
                        set_equipment(units_list, True, False, False)
                    if param_list[1] == "cellular_radio":
                        set_equipment(units_list, False, True, False)
                    if param_list[1] == "satellite_link":
                        set_equipment(units_list, False, False, True)
                elif function_name == "create_cellular_region":
                    position_list = generate_position_list(param_list[0], self.var_to_position)
                    polygon = Polygon(position_list)
                    self.cellular_zones.append(polygon)
                elif function_name == "create_position":
                    position = generate_position(param_list[0], self.var_to_position)
                    self.var_to_position[initialized_variable] = position
                elif function_name == "create_position_list":
                    position_list = generate_position_list(param_list[0])
                    self.var_to_position[initialized_variable] = position_list
                elif function_name == "create_group":
                    units_in_group = []
                    for param in param_list:
                        units_list = convert_to_units_list(param, self.var_to_units, self.var_to_group)
                        units_in_group.extend(units_list)
                    group_created = self.units_controller.create_group(units_in_group)
                    self.var_to_group[initialized_variable] = group_created
                elif function_name == "set_starting_position":
                    units_list = convert_to_units_list(param_list[0], self.var_to_units, self.var_to_group)
                    starting_position = generate_position(param_list[1], self.var_to_position)
                    set_starting_positions(units_list, starting_position)
                elif function_name == "set_waypoints":
                    units_list = convert_to_units_list(param_list[0], self.var_to_units, self.var_to_group)
                    position_list = generate_position_list(param_list[1], self.var_to_position)
                    set_waypoints(units_list, position_list)

    def get_cellular_zones(self):
        return self.cellular_zones

    def get_time_duration(self):
        return self.time_duration

    def get_time_step(self):
        return self.time_step
