from mobscript import *


load_map("map.json")
set_attribute("time_duration", 30)
set_attribute("time_step", 1)

a = create_units("pedestrian", "type_a", 1)
set_waypoints(a, [(50,0), (50, 90)])