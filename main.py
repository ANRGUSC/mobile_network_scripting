import graph_analyzer
from units_controller import *
from data_structures.unit import Unit
from simulation import Simulation
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from data_structures.instruction_line import InstructionLine
import re

def convert_to_units_list(key, var_to_units, var_to_group):
    if key in var_to_units:
        return var_to_units[key]
    elif key in var_to_group:
        return var_to_group[key].units_list

if __name__ == '__main__':
    units_controller = UnitsController()

    var_to_units = {}
    var_to_group = {}
    var_to_position = {}

    with open("input_data/instructions.txt") as instruction_file:
        for line in instruction_file:
            instruction_line = InstructionLine(line)
            initialized_variable = instruction_line.initialized_variable
            function_name = instruction_line.function_name
            param_list = instruction_line.param_list
            if function_name == "create_units":
                unit_name = param_list[0]
                unit_type = param_list[1]
                unit_count = int(param_list[2])
                units_created = units_controller.create_unit(unit_name, unit_type, unit_count)
                var_to_units[initialized_variable] = units_created
            elif function_name == "create_position":
                position_x = float(param_list[0])
                position_y = float(param_list[1])
                var_to_position[initialized_variable] = (position_x, position_y)
            elif function_name == "create_group":
                units_in_group = []
                for param in param_list:
                    units_list = convert_to_units_list(param, var_to_units, var_to_group)
                    units_in_group.extend(units_list)
                group_created = units_controller.create_group(units_in_group)
                var_to_group[initialized_variable] = group_created

    #units_controller.create_unit("pedestrian", "type_a", 1)


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