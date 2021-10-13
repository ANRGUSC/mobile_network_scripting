import math
from data_structures.change_equip_instruct import ChangeEquipInstruct

class DelayedInstructions:
    stop_movement = {}
    change_equipment = []

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

    def add_change_equipment(self, unit_list, time, turn_on, has_standard_radio,
                has_cellular_radio, has_satellite_link):
        self.change_equipment.append(ChangeEquipInstruct(unit_list, time, turn_on, has_standard_radio,
                has_cellular_radio, has_satellite_link))

    def get_change_equip_time(self):
        return self.change_equipment[0].time if self.change_equipment else math.inf

    def get_change_equip_instruct(self):
        return self.change_equipment[0]
        
    def pop_change_equip_instruct(self):
        self.change_equipment.pop(0)

    def initialize(self):
        for unit_key, time_list in self.stop_movement.items():
            self.stop_movement[unit_key].sort()
        self.change_equipment.sort(key=lambda x: x.time)
        
    