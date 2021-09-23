import graph_analyzer
from data_structures.global_attributes import *
from delayed_instructions import *
from instructions_parser import InstructionsParser
from units_controller import *
from map_controller import *
from simulation import Simulation
from program_state import ProgramState



if __name__ == '__main__':
    program_state = ProgramState()
    program_state.load_data_files("input_data/unit_types.json")
    program_state.parse_instruction_file("input_data/instructions.txt")
    program_state.save_state("program_states/state.txt")
    
    global_attributes = program_state.global_attributes
    units_controller = program_state.units_controller
    map_controller = program_state.map_controller
    delayed_instructions = program_state.delayed_instructions

    units_controller.initialize_units()
    delayed_instructions.initialize()

    simulation = Simulation(units_controller, map_controller, delayed_instructions)
    positions_history = simulation.run_simulation(global_attributes.time_step, global_attributes.time_duration)
    networks_data = graph_analyzer.run_graph_analysis(positions_history,
                                                      units_controller, map_controller, global_attributes, delayed_instructions)

    units_controller.save_generated_data()
    simulation.save_generated_data()
    graph_analyzer.save_generated_data(networks_data)
