from data_structures.global_attributes import *
from units_controller import *
from map_controller import *
from simulation import Simulation
from delayed_instructions import *
from instructions_parser import InstructionsParser

class ProgramState:
    def __init__(self, unit_types_file, map_file, global_attributes_file):
        self.instruction_var = {}
        self.global_attributes = GlobalAttributes(global_attributes_file)
        self.units_controller = UnitsController(unit_types_file)
        self.map_controller = MapController(map_file)
        self.delayed_instructions = DelayedInstructions()
        self.instructions_parser = InstructionsParser(self.instruction_var, self.units_controller, 
                self.map_controller, self.global_attributes, self.delayed_instructions)

    def parse_instruction_file(self, file_name):
        self.instructions_parser.parse_file(file_name)

    def save_state(self, file_name):
        print("Saving state to file")

    def load_state(self, file_name):
        print("Loading state")

