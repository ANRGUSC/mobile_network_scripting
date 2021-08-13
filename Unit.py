from enum import Enum

class Unit:
    def __init__(self, key, name, unit_type, starting_position, waypoints):
        self.key = key
        self.name = name
        self.unit_type = unit_type
        self.starting_position = starting_position
        self.waypoints = waypoints

    def encode(self):
        return self.__dict__
