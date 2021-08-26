from enum import Enum

class Unit:
    def __init__(self, key, name, unit_type, has_standard_radio, has_cellular_radio, has_satellite_link, starting_position, waypoints):
        self.key = key
        self.name = name
        self.unit_type = unit_type
        self.has_standard_radio = has_standard_radio
        self.has_cellular_radio = has_cellular_radio
        self.has_satellite_link = has_satellite_link
        self.starting_position = starting_position
        self.waypoints = waypoints

    def encode(self):
        return self.__dict__
