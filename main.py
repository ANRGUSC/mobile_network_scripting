import graph_analyzer
from units_controller import *
from data_structures.unit import Unit
from simulation import Simulation
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

if __name__ == '__main__':
    units_controller = UnitsController()
    unit_1 = Unit(1, "a", "a", False, True, False, (0, 0), [(1, 1), (3, 3), (5, 5)])
    unit_2 = Unit(2, "b", "b", False, True, False, (0, 0), [(1, 1), (3, 3), (5, 5)])
    unit_3 = Unit(3, "c", "c", False, True, False, (0, 0), [(10, 10), (20, 20), (30, 30)])
    unit_4 = Unit(4, "d", "d", False, True, False, (0, 0), [(10, 10), (20, 20), (30, 30)])
    units_controller.add_unit(unit_1)
    units_controller.add_unit(unit_2)
    units_controller.add_unit(unit_3)
    # units_controller.add_unit(unit_4)
    units_controller.save_data()

    simulation = Simulation(units_controller)
    positions_history = simulation.run_simulation(1, 10)
    simulation.save_data()

    # cellular_zones = [Polygon[(0, 0), (0, 10), (10, 10), (10, 0)]]
    cellular_zones = []
    polygon = Polygon([(0, 0), (0, 10), (10, 10), (10, 0)])
    cellular_zones.append(polygon)
    graph_analyzer.run_graph_analysis(positions_history, units_controller, cellular_zones)