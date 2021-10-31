from mobscript import *

load_map("map.json")

set_attribute("time_duration", 10)
set_attribute("time_step", 1)

p = create_units("pedestrian", "type_a", 1)
home = (0, 0)
set_starting_position(p, home)
set_waypoints(p, [(10,10)], 0, 10)

change_equipment_at_time(p, 1.0, False, "standard_radio")
change_equipment_at_time(p, 3.0, True, "standard_radio")
change_equipment_at_time(p, 5.0, False, "standard_radio")

change_equipment_at_time(p, 1.0, False, "satellite_link")
change_equipment_at_time(p, 3.0, True, "satellite_link")
change_equipment_at_time(p, 5.0, False, "satellite_link")

change_equipment_at_time(p, 5.0, False, "cellular_radio")
change_equipment_at_time(p, 9.0, True, "cellular_radio")
change_equipment_at_time(p, 10.0, False, "cellular_radio")
