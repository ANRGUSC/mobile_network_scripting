from mobscript import *

load_map("map.json")

set_attribute("time_duration", 10)
set_attribute("time_step", 1)

p = create_units("pedestrian", "type_a", 1)
u = create_units("UAV", "type_b", 1)
v = create_units("vehicle", "type_c", 2)
c = create_units("compute", "type_a", 3)
group_1 = create_group(p, c)

home = (15, 25)
set_starting_position(p, home)
set_waypoints(v, [(20,20), (50,50)], 7, 9)
set_waypoints(v, [(0,0), (10,0)], 0, 4)
stop_movement(v, 3)
change_equipment_at_time(u, 3.0, True, "standard_radio")
change_equipment_at_time(v, 5.0, False, "standard_radio")

create_cellular_region([(0,0), (10,0), (20,10), (10,30), (0,30)])
