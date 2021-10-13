import graph_analyzer
from simulation import Simulation
from program_state import ProgramState
from argparse import ArgumentParser
from display_controller import DisplayController


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-w", "--workspace", dest="workspace",
                    help="folder that includes instructions and outputs", metavar="WORKSPACE")
    args = parser.parse_args()

    program_state = ProgramState("input_data_defaults/unit_types.json", "input_data_defaults/map.json",
            "input_data_defaults/global_attributes.json")
    program_state.parse_instruction_file(args.workspace + "/instructions.txt")
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

    units_controller.save_generated_data(args.workspace + "/generated_data/units.json")
    simulation.save_generated_data(args.workspace + "/generated_data/simulation.json")
    graph_analyzer.save_generated_data(args.workspace + "/generated_data/networks.json", networks_data)

    display_controller = DisplayController(units_controller, map_controller, positions_history, global_attributes)
    display_controller.display()
