import graph_analyzer
from data_structures.global_attributes import *
from data_structures.delayed_instructions import *
from instructions_parser import InstructionsParser
from units_controller import *
from map_controller import *
from simulation import Simulation


if __name__ == '__main__':
    global_attributes = GlobalAttributes()
    units_controller = UnitsController()
    map_controller = MapController()
    delayed_instructions = DelayedInstructions()

    instructions_parser = InstructionsParser(units_controller, map_controller, global_attributes, delayed_instructions)
    instructions_parser.parse_file("input_data/instructions.txt")

    units_controller.initialize_units()
    delayed_instructions.initialize()

    simulation = Simulation(units_controller, map_controller, delayed_instructions)
    positions_history = simulation.run_simulation(global_attributes.time_step, global_attributes.time_duration)
    networks_data = graph_analyzer.run_graph_analysis(positions_history,
                                                      units_controller, map_controller, global_attributes.standard_radio_radius)

    units_controller.save_data()
    simulation.save_data()
    graph_analyzer.save_data(networks_data)
