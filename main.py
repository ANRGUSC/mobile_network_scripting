import graph_analyzer
from data_structures.global_attributes import *
from instructions_parser import InstructionsParser
from units_controller import *
from simulation import Simulation


if __name__ == '__main__':
    units_controller = UnitsController()

    global_attributes = GlobalAttributes()
    instructions_parser = InstructionsParser(units_controller, global_attributes)
    instructions_parser.parse_file("input_data/instructions.txt")
    cellular_zones = instructions_parser.get_cellular_zones()

    units_controller.initialize_units()
    simulation = Simulation(units_controller)
    positions_history = simulation.run_simulation(global_attributes.time_step, global_attributes.time_duration)
    networks_data = graph_analyzer.run_graph_analysis(positions_history,
                                                      units_controller, cellular_zones, global_attributes.standard_radio_radius)

    units_controller.save_data()
    simulation.save_data()
    graph_analyzer.save_data(networks_data)
