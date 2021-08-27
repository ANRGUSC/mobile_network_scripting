def set_waypoints(units_list, waypoints):
    for unit in units_list:
        unit.waypoints = waypoints


def set_starting_positions(units_list, starting_position):
    for unit in units_list:
        unit.starting_position = starting_position


def set_equipment(units_list, has_standard_radio, has_cellular_radio, has_satellite_link):
    for unit in units_list:
        unit.set_equipment(has_standard_radio, has_cellular_radio, has_satellite_link)
