from argparse import ArgumentParser
import pathlib
import os 

from mobscript import Instance 

from .graph_analyzer import run_graph_analysis, save_generated_data
from .simulation import Simulation
from .display_controller import DisplayController

thisdir = pathlib.Path(__file__).resolve().parent


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "path",
        metavar="PATH",
        help="path to instructions file",
    )
    parser.add_argument(
        "-o", "--out",
        metavar="PATH",
        default=pathlib.Path(os.getcwd()).joinpath("generated_data"),
        help="path to write outputs to (should either not exist or be a directory)"
    )
    return parser 

def main():
    parser = get_parser()
    args = parser.parse_args()

    path = pathlib.Path(args.path).resolve(strict=True)
    outpath = pathlib.Path(args.out).resolve()
    assert(not outpath.is_file())

    Instance.load_script(path)
    
    global_attributes = Instance.global_attributes
    units_controller = Instance.units_controller
    map_controller = Instance.map_controller
    delayed_instructions = Instance.delayed_instructions

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

    outpath.mkdir(exist_ok=True, parents=True)
    units_controller.save_generated_data(
        outpath.joinpath("units.json")
    )
    simulation.save_generated_data(
        outpath.joinpath("simulation.json")
    )
    save_generated_data(
        outpath.joinpath("networks.json"),
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