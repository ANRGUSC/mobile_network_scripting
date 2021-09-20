import math

class DelayedInstructions:
    stop_movement = {}

    def add_stop_movement(self, unit_list, time):
        for unit in unit_list:
            unit_key = unit.key
            time_list = self.stop_movement[unit_key] if unit_key in self.stop_movement else []
            time_list.append(time)
            self.stop_movement[unit_key] = time_list

    def get_stop_movement_time(self, unit_key):
        if unit_key not in self.stop_movement or not self.stop_movement[unit_key]:
            return math.inf
        return self.stop_movement[unit_key][0]

    def remove_stop_movement_time(self, unit_key):
        self.stop_movement[unit_key].pop(0)

    def initialize(self):
        for unit_key, time_list in self.stop_movement.items():
            self.stop_movement[unit_key].sort()
        
    