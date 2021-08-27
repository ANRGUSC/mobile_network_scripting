import json
import networkx as nx
from networkx.readwrite import json_graph
from util.file_operations import create_blank_file
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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

def run_graph_analysis(positions_history, units_controller, cellular_zones):
    create_blank_file("generated_data", "networks.json")
    graph_template = nx.Graph()
    units_data = units_controller.get_units_data()
    for key, value in units_data.items():
        graph_template.add_node(key, has_standard_radio=value.has_cellular_radio,
                                has_cellular_radio=value.has_cellular_radio,
                                has_satellite_link=value.has_satellite_link)
    create_satellite_edges(graph_template)

    networks_data = []
    for time_frame in positions_history:
        graph = graph_template.copy()

        for key, value in time_frame.items():
            graph.nodes[key]["coord"] = value

        create_cellular_radio_edges(graph, cellular_zones)

        # Print serializable graph data
        graph_data = json_graph.node_link_data(graph)
        networks_data.append(json.dumps(graph_data))

    with open("generated_data/networks.json", "w") as outfile:
        json.dump(networks_data, outfile, default=lambda o: o.encode(), indent=4)
