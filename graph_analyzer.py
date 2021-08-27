import json
import networkx as nx
import math
from networkx.readwrite import json_graph
from util.file_operations import create_blank_file
from shapely.geometry import Point


def calculate_dist_between_points(point_1, point_2):
    return math.sqrt(((point_1[0] - point_2[0]) ** 2) + ((point_1[1] - point_2[1]) ** 2))


def create_clique_from_nodes(graph, nodes):
    for current_index in range(len(nodes)):
        for next_index in range(current_index + 1, len(nodes)):
            graph.add_edge(nodes[current_index], nodes[next_index])


def create_satellite_edges(graph):
    nodes_with_satellite = [x for x, y in graph.nodes(data=True) if y['has_satellite_link'] == True]
    create_clique_from_nodes(graph, nodes_with_satellite)


def create_cellular_radio_edges(graph, cellular_zones):
    nodes = []
    coords = nx.get_node_attributes(graph, 'coord')
    has_cellular_radio_list = nx.get_node_attributes(graph, 'has_cellular_radio')
    for node in graph.nodes:
        if has_cellular_radio_list[node]:
            for zone in cellular_zones:
                if zone.contains(Point(coords[node])):
                    nodes.append(node)
                    break
    create_clique_from_nodes(graph, nodes)


def create_standard_radio_edges(graph, standard_radio_radius):
    nodes_with_radios = [x for x, y in graph.nodes(data=True) if y['has_standard_radio'] == True]
    for current_index in range(len(nodes_with_radios)):
        for next_index in range(current_index + 1, len(nodes_with_radios)):
            current_node_key = nodes_with_radios[current_index]
            next_node_key = nodes_with_radios[next_index]
            current_node = graph.nodes[nodes_with_radios[current_index]]
            next_node = graph.nodes[nodes_with_radios[next_index]]
            if calculate_dist_between_points(current_node["coord"], next_node["coord"]) < standard_radio_radius:
                graph.add_edge(current_node_key, next_node_key)


def run_graph_analysis(positions_history, units_controller, cellular_zones, standard_radio_radius):
    create_blank_file("generated_data", "networks.json")
    graph_template = nx.Graph()
    units_data = units_controller.get_units_data()
    for key, value in units_data.items():
        graph_template.add_node(key, has_standard_radio=value.has_standard_radio,
                                has_cellular_radio=value.has_cellular_radio,
                                has_satellite_link=value.has_satellite_link)
    create_satellite_edges(graph_template)

    networks_data = []
    for time_frame in positions_history:
        graph = graph_template.copy()

        for key, value in time_frame.items():
            graph.nodes[key]["coord"] = value

        create_cellular_radio_edges(graph, cellular_zones)
        create_standard_radio_edges(graph, standard_radio_radius)

        # Print serializable graph data
        graph_data = json_graph.node_link_data(graph)
        networks_data.append(json.dumps(graph_data))
    return networks_data


def save_data(networks_data):
    with open("generated_data/networks.json", "w") as outfile:
        json.dump(networks_data, outfile, default=lambda o: o.encode(), indent=4)
