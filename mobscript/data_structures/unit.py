from typing import Any, Dict, List, Tuple, Union


class Unit:
    def __init__(self, 
                 key: str, 
                 name: str, 
                 unit_type: int, 
                 starting_position: Tuple[Union[int, float], Union[int, float]] = (0, 0), 
                 waypoints: List[Tuple[Union[int, float], Union[int, float]]] = [], 
                 has_standard_radio: bool = False,
                 has_cellular_radio: bool = False, 
                 has_satellite_link: bool = False) -> None:
        self.key = key
        self.name = name
        self.unit_type = unit_type
        self.has_standard_radio = has_standard_radio
        self.has_cellular_radio = has_cellular_radio
        self.has_satellite_link = has_satellite_link
        self.starting_position = starting_position
        self.waypoints = waypoints
        self.waypoints_timeline: List[Dict[str, Any]] = []

    def encode(self) -> Dict[str, Any]:
        return self.__dict__

    def set_equipment(self, 
                      has_standard_radio: bool, 
                      has_cellular_radio: bool, 
                      has_satellite_link: bool) -> None:
        self.has_standard_radio = has_standard_radio
        self.has_cellular_radio = has_cellular_radio
        self.has_satellite_link = has_satellite_link

    def initialize(self) -> None:
        self.waypoints_timeline.sort(key=lambda x: x["start_time"])
