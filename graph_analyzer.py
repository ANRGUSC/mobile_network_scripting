import json
from pathlib import Path
import networkx as nx
from networkx.readwrite import json_graph
from util.file_operations import create_blank_file

def run_graph_analysis(positions_history, units_controller):

    create_blank_file("generated_data", "networks.json")
    graph_template = nx.Graph()
    units_data = units_controller.get_units_data()
    for key, value in units_data.items():
        graph_template.add_node(key, has_standard_radio=value.has_cellular_radio,
                                has_cellular_radio=value.has_cellular_radio, has_satellite_link=value.has_satellite_link)

    networks_data = []
    for time_frame in positions_history:
        # handle sattelite connections
        graph = graph_template.copy()

        # Graph = nx.Graph()
        # Graph.add_node(1)
        # Graph.add_node(2)
        # Graph.add_node(3)
        # Graph.add_node(4)
        # Graph.add_node(5)
        # Graph.add_edges_from([(1,2),(2,3),(4,5)])

        graph_data = json_graph.node_link_data(graph)
        networks_data.append(json.dumps(graph_data))

    with open("generated_data/networks.json", "w") as outfile:
        json.dump(networks_data, outfile, default=lambda o: o.encode(), indent=4)