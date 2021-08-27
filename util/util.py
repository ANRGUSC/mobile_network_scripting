def set_waypoints(units_list, waypoints):
    for unit in units_list:
        unit.waypoints = waypoints


def set_starting_positions(units_list, starting_position):
    for unit in units_list:
        unit.starting_position = starting_position


def set_equipment(units_list, has_standard_radio, has_cellular_radio, has_satellite_link):
    for unit in units_list:
        unit.set_equipment(has_standard_radio, has_cellular_radio, has_satellite_link)


def split_list_with_braces(string_to_split):
    trailing_index = 0
    param_list = []
    paren_count = 0
    bracket_count = 0
    for index, char in enumerate(string_to_split):
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
        elif char == ',':
            if paren_count == 0 and bracket_count == 0:
                param_list.append(string_to_split[trailing_index:index])
                trailing_index = index + 1
    param_list.append(string_to_split[trailing_index:len(string_to_split)])
    return param_list
