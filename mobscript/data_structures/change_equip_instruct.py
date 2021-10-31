# Turns all equipment on or off depending on turn_on
# If an equipment piece's variable is false, that it is unchanged
# Setting an equipment to True means that the value is allowed to change,
# but does not necessarily change it

from typing import List


class ChangeEquipInstruct:
    def __init__(self, 
                 key_list: List[str], 
                 time: int, 
                 turn_on: bool, 
                 modify_standard_radio: bool,
                 modify_cellular_radio: bool, 
                 modify_satellite_link: bool):
        self.key_list = key_list
        self.time = time
        self.turn_on = turn_on
        self.modify_standard_radio = modify_standard_radio
        self.modify_cellular_radio = modify_cellular_radio
        self.modify_satellite_link = modify_satellite_link