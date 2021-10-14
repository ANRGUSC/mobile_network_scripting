from typing import Any, Dict, List

from .unit import Unit

class Group:
    def __init__(self, key: str, units_list: List[Unit]) -> None:
        self.key = key
        self.units_list = units_list

    def encode(self) -> Dict[str, Any]:
        return self.__dict__
