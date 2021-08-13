from unit_data_api import *
from Unit import Unit
from simulation import Simulation

if __name__ == '__main__':
    unit_data = UnitData()
    unit_1 = Unit(1, "a", 1, (0, 0), [(1, 1), (2, 2), (3, 3)])
    unit_2 = Unit(2, "b", 2, (0, 0), [(1, 1), (2, 2), (3, 3)])
    unit_3 = Unit(3, "c", 3, (0, 0), [(1, 1), (2, 2), (3, 3)])
    unit_data.add_unit(unit_1)
    unit_data.add_unit(unit_2)
    unit_data.add_unit(unit_3)
    unit_data.save_data()

    simulation = Simulation(unit_data)
    simulation.run_simulation(0.01, 100)
    simulation.save_data()