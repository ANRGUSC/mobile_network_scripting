import graph_analyzer
from instructions_parser import InstructionsParser
from units_controller import *
from simulation import Simulation


if __name__ == '__main__':
    units_controller = UnitsController()

    # Default values, unless set directly in instructions
    # Find a better way to store defaults and update these from the instructions parser
    time_duration = 10
    time_step = 1
    standard_radio_radius = 3

    instructions_parser = InstructionsParser(units_controller)
    instructions_parser.parse_file("input_data/instructions.txt")

    cellular_zones = instructions_parser.get_cellular_zones()
    # Pass up time values from parser to the main file
    # time_duration = instructions_parser.get_time_duration()
    # time_step = instructions_parser.get_time_step()

    simulation = Simulation(units_controller)
    positions_history = simulation.run_simulation(time_step, time_duration)
    networks_data = graph_analyzer.run_graph_analysis(positions_history,
                                                      units_controller, cellular_zones, standard_radio_radius)

    units_controller.save_data()
    simulation.save_data()
    graph_analyzer.save_data(networks_data)
