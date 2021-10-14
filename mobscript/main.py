from argparse import ArgumentParser
import pathlib 

from .graph_analyzer import run_graph_analysis, save_generated_data
from .simulation import Simulation
from .program_state import ProgramState
from .display_controller import DisplayController

thisdir = pathlib.Path(__file__).resolve().parent

def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-w", "--workspace",
        required=True,
        metavar="WORKSPACE",
        help="folder that includes instructions and outputs",
    )
    args = parser.parse_args()

    program_state = ProgramState(
        thisdir.joinpath("input_data_defaults", "unit_types.json"),
        thisdir.joinpath("input_data_defaults", "map.json"),
        thisdir.joinpath("input_data_defaults", "global_attributes.json") 
    )

    program_state.parse_instruction_file(
        pathlib.Path(args.workspace).joinpath("instructions.txt")
    )
    
    global_attributes = program_state.global_attributes
    units_controller = program_state.units_controller
    map_controller = program_state.map_controller
    delayed_instructions = program_state.delayed_instructions

    units_controller.initialize_units()
    delayed_instructions.initialize()

    simulation = Simulation(units_controller, map_controller, delayed_instructions)
    positions_history = simulation.run_simulation(global_attributes.time_step, global_attributes.time_duration)
    networks_data = run_graph_analysis(
        positions_history,
        units_controller, 
        map_controller, 
        global_attributes, 
        delayed_instructions
    )

    units_controller.save_generated_data(args.workspace + "/generated_data/units.json")
    simulation.save_generated_data(args.workspace + "/generated_data/simulation.json")
    save_generated_data(args.workspace + "/generated_data/networks.json", networks_data)

    display_controller = DisplayController(units_controller, map_controller, positions_history, global_attributes)
    display_controller.display()


if __name__ == "__main__":
    main()