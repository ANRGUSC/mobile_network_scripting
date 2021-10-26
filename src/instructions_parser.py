import math
from shapely.geometry.polygon import Polygon
from data_structures.instruction_line import InstructionLine
from util.util import set_equipment


class InstructionsParser:
    def __init__(self, instruction_var, units_controller, map_controller, global_attributes, delayed_instructions):
        self.instruction_var = instruction_var
        self.units_controller = units_controller
        self.map_controller = map_controller
        self.global_attributes = global_attributes
        self.delayed_instructions = delayed_instructions

    def convert_unit_list_to_key_list(self, unit_list):
        unit_keys = []
        for unit in unit_list:
            unit_keys.append(unit.key)
        return unit_keys

    def handle_function(self, initialized_variable, function_name, param_list):
        if function_name == "create_units":
            unit_name = param_list[0]
            unit_type = param_list[1]
            unit_count = param_list[2]
            units_created = self.units_controller.create_unit(unit_name, unit_type, unit_count)
            self.instruction_var[initialized_variable] = units_created
        elif function_name == "set_attribute":
            attribute = param_list[0]
            value = param_list[1]
            if attribute == "time_step":
                self.global_attributes.time_step = value
            elif attribute == "time_duration":
                self.global_attributes.time_duration = value
            elif attribute == "standard_radio_radius":
                self.global_attributes.standard_radio_radius = value
        elif function_name == "equip":
            units_list = param_list[0]
            if param_list[1] == "standard_radio":
                set_equipment(units_list, True, False, False)
            if param_list[1] == "cellular_radio":
                set_equipment(units_list, False, True, False)
            if param_list[1] == "satellite_link":
                set_equipment(units_list, False, False, True)
        elif function_name == "create_cellular_region":
            position_list = param_list[0]
            polygon = Polygon(position_list)
            self.map_controller.add_cellular_zone(polygon)
        elif function_name == "create_group":
            units_in_group = []
            for param in param_list:
                units_list = param
                units_in_group.extend(units_list)
            group_created = self.units_controller.create_group(units_in_group)
            self.instruction_var[initialized_variable] = group_created
        elif function_name == "set_starting_position":
            units_list = param_list[0]
            starting_position = param_list[1]
            for unit in units_list:
                unit.starting_position = starting_position
        elif function_name == "set_waypoints":
            units_list = param_list[0]
            waypoints = param_list[1]
            start_time = param_list[2] if len(param_list) >= 3 else 0
            end_time = param_list[3] if len(param_list) >= 4 else math.inf
            for unit in units_list:
                unit.waypoints_timeline.append({
                    "waypoints": waypoints,
                    "start_time": start_time,
                    "end_time": end_time
                })
        elif function_name == "load_map":
            file_name = param_list[0]
            self.map_controller.load_map(file_name)
        elif function_name == "stop_movement":
            units_list = param_list[0]
            time = param_list[1]
            self.delayed_instructions.add_stop_movement(units_list, time)
        elif function_name == "change_equipment_at_time":
            units_list = param_list[0]
            time = param_list[1]
            turn_on = param_list[2]
            equipment_name = param_list[3]
            self.delayed_instructions.add_change_equipment(self.convert_unit_list_to_key_list(units_list), 
                    time, turn_on, equipment_name=="standard_radio", 
                    equipment_name=="cellular_radio", equipment_name=="satellite_link")


    def parse_file(self, file_name):
        with open(file_name) as instructions_file:
            for line in instructions_file:
                if not line.strip():
                    continue
                instruction_line = InstructionLine(line, self.instruction_var)
                initialized_variable = instruction_line.initialized_variable
                function_name = instruction_line.function_name
                param_list = instruction_line.param_list
                rhs_value = instruction_line.rhs_value

                # delete
                # print(initialized_variable, function_name, param_list)
                # delete

                if function_name is not None:
                    self.handle_function(initialized_variable, function_name, param_list)
                elif initialized_variable is not None and rhs_value is not None:
                    self.instruction_var[initialized_variable] = rhs_value
