import graph_analyzer
from units_controller import *
from simulation import Simulation
from shapely.geometry.polygon import Polygon
from data_structures.instruction_line import InstructionLine
import re
import util.util


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
    return split[0], split[1]


if __name__ == '__main__':
    units_controller = UnitsController()

    var_to_units = {}
    var_to_group = {}
    var_to_position = {}

    with open("input_data/instructions.txt") as instruction_file:
        for line in instruction_file:
            if not line.strip():
                continue
            instruction_line = InstructionLine(line)
            initialized_variable = instruction_line.initialized_variable
            function_name = instruction_line.function_name
            param_list = instruction_line.param_list

            print(initialized_variable, function_name, param_list, flush=True)

            if function_name == "create_units":
                unit_name = param_list[0]
                unit_type = param_list[1]
                unit_count = int(param_list[2])
                units_created = units_controller.create_unit(unit_name, unit_type, unit_count)
                var_to_units[initialized_variable] = units_created
            elif function_name == "equip":
                units_list = convert_to_units_list(param_list[0], var_to_units, var_to_group)
                if param_list[1] == "standard_radio":
                    util.util.set_equipment(units_list, True, False, False)
                if param_list[1] == "cellular_radio":
                    util.util.set_equipment(units_list, False, True, False)
                if param_list[1] == "satellite_link":
                    util.util.set_equipment(units_list, False, False, True)
            # elif function_name == "create_cellular_region":
            #     position_list = generate_position_list(param_list[0])
            elif function_name == "create_position":
                position = generate_position(param_list[0], var_to_position)
                var_to_position[initialized_variable] = position
            elif function_name == "create_group":
                units_in_group = []
                for param in param_list:
                    units_list = convert_to_units_list(param, var_to_units, var_to_group)
                    units_in_group.extend(units_list)
                group_created = units_controller.create_group(units_in_group)
                var_to_group[initialized_variable] = group_created
            elif function_name == "set_starting_position":
                units_list = convert_to_units_list(param_list[0], var_to_units, var_to_group)
                starting_position = generate_position(param_list[1], var_to_position)
                util.util.set_starting_positions(units_list, starting_position)

    # units_controller.create_unit("pedestrian", "type_a", 1)

    # units_controller.create_unit("name_a", "type_a", 1, (0, 0), [(1, 1), (3, 3), (5, 5)], True)
    # units_controller.create_unit("name_b", "type_b", 1, (0, 0), [(1, 1), (3, 3), (5, 5)], True)
    # units_controller.create_unit("name_c", "type_c", 1, (0, 0), [(10, 10), (20, 20), (30, 30)], True)
    # units_controller.create_unit("name_d", "type_a", 1, (0, 0), [(10, 10), (20, 20), (30, 30)], True)
    units_controller.save_data()

    simulation = Simulation(units_controller)
    positions_history = simulation.run_simulation(1, 10)
    simulation.save_data()

    cellular_zones = []
    polygon = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    cellular_zones.append(polygon)
    standard_radio_radius = 3
    graph_analyzer.run_graph_analysis(positions_history, units_controller, cellular_zones, standard_radio_radius)
