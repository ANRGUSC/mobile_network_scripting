import json
from pathlib import Path
import networkx as nx
from networkx.readwrite import json_graph

def run_graph_analysis(positions_history, units_controller):
    network_file = Path("generated_data/networks.json")
    if network_file.is_file() is False:
        with open("generated_data/networks.json", "w") as outfile:
            template = {}
            json.dump(template, outfile)
    networks_data = []

    for time_frame in positions_history:
        Graph = nx.Graph()
        Graph.add_node(1)
        Graph.add_node(2)
        Graph.add_node(3)
        Graph.add_node(4)
        Graph.add_node(5)
        Graph.add_edges_from([(1,2),(2,3),(4,5)])

        data1 = json_graph.node_link_data(Graph)
        networks_data.append(json.dumps(data1))

    with open("generated_data/networks.json", "w") as outfile:
        json.dump(networks_data, outfile, default=lambda o: o.encode(), indent=4)