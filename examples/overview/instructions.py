from mobscript import *
import pygame
graph=load_map("map.json")

set_attribute("time_duration", 10)
set_attribute("time_step", 1)

#p = create_units("pedestrian", "type_a", 1, False)
u = create_units("UAV", "type_b", 1, True)
u_2 = create_units("UAV", "type_b", 1, True)
u_3 = create_units("UAV", "type_b", 1, True)
v = create_units("vehicle", "type_c", 1, True)
c = create_units("compute", "type_a", 1, True)
#group_1 = create_group(p, c)

home = (10,0)
set_starting_position(u, home)
set_waypoints(v, [(20,20), (50,50)], 0,1)
set_waypoints(u_2, [(15,25), (20,15)], 0,1)
set_waypoints(u_3, [(35,30), (30,32)], 0,2)
set_waypoints(v, [(40,15), (10,0)],0,2)
set_waypoints(c, [(0,0), (10,10)],1,3)
stop_movement(v, 3)
create_cellular_region([(0,0), (10,0), (20,10), (10,30), (0,30)])
