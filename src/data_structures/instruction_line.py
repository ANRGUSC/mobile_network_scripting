import re
from util.util import split_list_with_braces
from data_structures.unit import Unit

def remove_quotes(value):
    return value.replace("\"", "")

def convert_to_units_list(value, var_to_position):
    split = list(filter(None, re.split(r'\[|\]', value)))
    var_name = split[0]
    if var_name in var_to_position:
        var_value = var_to_position[var_name]
        if type(var_value) is Unit.__class__:
            units_list = var_to_position[var_name]
        else:
            units_list = var_to_position[var_name].units_list
    if len(split) == 1:
        return units_list
    index_range = split[1].split(":")
    return units_list[int(index_range[0]):int(index_range[1])]


def generate_position(value, var_to_position):
    if value in var_to_position:
        return var_to_position[value]
    split = list(filter(None, re.split(r'\(|\)|,', value)))
    return float(split[0]), float(split[1])

def generate_list(value, var_to_position):
    if value in var_to_position:
        return var_to_position[value]
    value = value[1:len(value) - 1]
    position_tuple_list = []
    for position_string in split_list_with_braces(value):
        position_tuple_list.append(generate_position(position_string, var_to_position))
    return position_tuple_list

def begins_and_ends_with(string, char_start, char_end):
    return  string[0] == char_start and string[-1]  == char_end

def convert_string_list_to_types(string_list, var_to_position):
    type_list = []
    for string in string_list:
        type_list.append(convert_string_to_type(string, var_to_position))
    return type_list

def convert_string_to_type(string, var_to_position):
    if string in var_to_position:
        return var_to_position[string]
    elif string == "True":
        return True
    elif string == "False":
        return False
    elif begins_and_ends_with(string, '\"', '\"'):
        return remove_quotes(string)
    elif begins_and_ends_with(string, '(', ')'):
        return generate_position(string, var_to_position)
    elif begins_and_ends_with(string, '[', ']'):
        return generate_list(string, var_to_position)
    elif string.isdigit():
        return int(string)
    elif string.replace('.','',1).isdigit():
        return float(string)
    return string


class InstructionLine:    
    def __init__(self, line, var_to_position):
        line = line.strip().replace(" ", "")
        split = re.split(r'=', line)
        if len(split) == 2:
            self.initialized_variable = split[0]
        else:
            self.initialized_variable = None

        post_equals = split[-1]
        function_pattern = re.compile("[a-z]+(.*?)$")

        if function_pattern.match(post_equals):
            self.rhs_value = None

            first_open_paren = post_equals.find('(')
            last_end_paren = post_equals.rfind(')')
            self.function_name = post_equals[0:first_open_paren]

            parameters = post_equals[first_open_paren + 1:last_end_paren]
            param_list = split_list_with_braces(parameters)
            param_list_values = convert_string_list_to_types(param_list, var_to_position)

            self.param_list = param_list_values if param_list_values else []    
        else:
            self.function_name = None
            self.param_list = None
            self.rhs_value = convert_string_to_type(post_equals, var_to_position)

