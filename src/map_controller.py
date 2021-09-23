from util.file_operations import load_json_from_file
import networkx as nx
from networkx.readwrite import json_graph
import json


def is_in_bounds(index, row_size, col_size):
    if index[0] < 0 or index[0] >= row_size:
        return False
    if index[1] < 0 or index[1] >= col_size:
        return False
    return True

class MapController:
    cellular_zones = []

    def __init__(self, file_name):
        self.load_map(file_name)

    def load_map(self, file_name):
        json = load_json_from_file(file_name)
        self.scale = json["metadata"]["scale"]
        self.map = json["map"]
        self.row_size = len(self.map)
        self.col_size = len(self.map[0])
        self.map_graph = self.construct_graph(self.map, self.row_size, self.col_size, self.scale)        

    def construct_graph(self, map, row_size, col_size, scale):
        graph = nx.Graph()
        for row in range(0, row_size + 1):
            for col in range(0, col_size + 1):
                index = (row, col)
                coord=(scale*row, scale*col)
                graph.add_node(index, coord=coord,
                        allowable_terrain=self.get_allowable_terrain(map, coord))
        for row in range(0, row_size):
            for col in range(0, col_size):
                top_mid = (row, col)
                top_right = (row, col+1)
                bot_left = (row+1, col-1)
                bot_mid = (row+1, col)
                bot_right = (row+1, col+1)
                if is_in_bounds(top_right, row_size+1, col_size+1):
                    graph.add_edge(top_mid, top_right)
                if is_in_bounds(bot_left, row_size+1, col_size+1):
                    graph.add_edge(top_mid, bot_left)
                if is_in_bounds(bot_mid, row_size+1, col_size+1):
                    graph.add_edge(top_mid, bot_mid)
                if is_in_bounds(bot_right, row_size+1, col_size+1):
                    graph.add_edge(top_mid, bot_right)
        return graph

    def add_cellular_zone(self, cellular_zone):
        self.cellular_zones.append(cellular_zone)

    def get_cellular_zones(self):
        return self.cellular_zones

    def get_allowable_terrain(self, map, coord):
        return ".r"

    def convert_position_to_index(self, point):
        return ((self.row_size*self.scale - point[0]) // self.scale, point[1] // self.scale)

    def add_points_as_nodes(self, graph_copy, points):
        nodes = []
        count = 0
        for point in points:
            index = self.convert_position_to_index(point)
            graph_copy.add_node(count, coord=point,
                    allowable_terrain=self.get_allowable_terrain(map, point))
            graph_copy.add_edge(index, count)
            nodes.append(count)
            count += 1
        return nodes

    def find_path_from_nodes(self, graph_copy, waypoint_keys):
        waypoints = []
        for waypoint_index in range(0, len(waypoint_keys) - 1):
            curr_node_key = waypoint_keys[waypoint_index]
            next_node_key = waypoint_keys[waypoint_index + 1]
            path = nx.shortest_path(graph_copy, source=curr_node_key, target=next_node_key)
            for path_index in range(0, len(path)):
                node_key = path[path_index]
                if waypoint_index != len(waypoint_keys)-2 and path_index == len(path)-1:
                    continue
                waypoints.append(graph_copy.nodes[node_key]["coord"])
        return waypoints

    def convert_waypoints_to_path(self, waypoints, allowable_terrain):
        graph_copy = self.map_graph.copy()
        waypoint_keys = self.add_points_as_nodes(graph_copy, waypoints)
        new_waypoints = self.find_path_from_nodes(graph_copy, waypoint_keys)
        print(new_waypoints)
        return new_waypoints

