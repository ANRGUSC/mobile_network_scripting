from typing import List

from ..data_structures.unit import Unit

def set_equipment(units_list: List[Unit], 
                  has_standard_radio: bool, 
                  has_cellular_radio: bool, 
                  has_satellite_link: bool) -> None:
    for unit in units_list:
        unit.set_equipment(has_standard_radio, has_cellular_radio, has_satellite_link)


def split_list_with_braces(string_to_split: str) -> List[str]:
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
