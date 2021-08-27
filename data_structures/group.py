class Group:
    def __init__(self, key, units_list):
        self.key = key
        self.units_list = units_list

    def encode(self):
        return self.__dict__

    # def set_starting_positions(self, starting_position):
    #     for unit in self.units_list:
    #         unit.starting_position = starting_position
    #
    # def set_waypoints(self, waypoints):
    #     for unit in self.units_list:
    #         unit.waypoints = waypoints
