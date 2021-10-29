from argparse import ArgumentParser
import pathlib

from mobscript import Instance 

from .graph_analyzer import run_graph_analysis, save_generated_data
from .simulation import Simulation
from .display_controller import DisplayController

thisdir = pathlib.Path(__file__).resolve().parent


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-w", "--workspace",
        required=True,
        metavar="WORKSPACE",
        help="folder that includes instructions and outputs",
    )
    return parser 

def main():
    parser = get_parser()
    args = parser.parse_args()

    workspace = pathlib.Path(args.workspace).resolve(strict=True)

    instance = Instance()
    instance.load_script(workspace.joinpath("instructions.py"))
    
    global_attributes = instance.global_attributes
    units_controller = instance.units_controller
    map_controller = instance.map_controller
    delayed_instructions = instance.delayed_instructions

    units_controller.initialize_units()
    delayed_instructions.initialize()

    simulation = Simulation(
        units_controller, 
        map_controller, 
        delayed_instructions
    )
    positions_history = simulation.run_simulation(
        global_attributes.time_step, 
        global_attributes.time_duration
    )
    networks_data = run_graph_analysis(
        positions_history,
        units_controller, 
        map_controller, 
        global_attributes, 
        delayed_instructions
    )

    units_controller.save_generated_data(
        workspace.joinpath("generated_data", "units.json")
    )
    simulation.save_generated_data(
        workspace.joinpath("generated_data", "simulation.json")
    )
    save_generated_data(
        workspace.joinpath("generated_data", "networks.json"),
        networks_data
    )

    display_controller = DisplayController(
        units_controller, 
        map_controller, 
        positions_history, 
        global_attributes
    )
    display_controller.display()


if __name__ == "__main__":
    main()