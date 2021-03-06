from mobscript import *

load_map("map.json")
set_attribute("time_duration", 15.0)
set_attribute("time_step", 1.0)

a = create_units("pedestrian", "type_a", 1)
b = create_units("UAV", "type_b", 1)
c = create_units("vehicle", "type_c", 1)

set_waypoints(a, [(5,5),(10,10),(15,15),(20,20)])
set_waypoints(b, [(20,20),(10,50)])
set_waypoints(c, [(20,20),(0,0),(20,20),(0,0)])