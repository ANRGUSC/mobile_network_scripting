import pathlib

from .data_structures.global_attributes import GlobalAttributes
from .units_controller import UnitsController
from .map_controller import MapController
from .delayed_instructions import DelayedInstructions
from .instructions_parser import InstructionsParser

class ProgramState:
    def __init__(self, 
                 unit_types_file: pathlib.Path, 
                 map_file: pathlib.Path, 
                 global_attributes_file: pathlib.Path) -> None:
        self.instruction_var = {}
        self.global_attributes = GlobalAttributes(pathlib.Path(global_attributes_file))
        self.units_controller = UnitsController(pathlib.Path(unit_types_file))
        self.map_controller = MapController(pathlib.Path(map_file))
        self.delayed_instructions = DelayedInstructions()
        self.instructions_parser = InstructionsParser(
            self.instruction_var, self.units_controller,
            self.map_controller, self.global_attributes,
            self.delayed_instructions
        )

    def parse_instruction_file(self, file_name: pathlib.Path) -> None:
        self.instructions_parser.parse_file(pathlib.Path(file_name))