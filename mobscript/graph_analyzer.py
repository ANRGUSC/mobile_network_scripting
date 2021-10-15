import json
import pathlib
from typing import Any, Dict, Hashable, Iterable, List, Tuple, Union
import networkx as nx
import math
from networkx.readwrite import json_graph
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from mobscript.data_structures.global_attributes import GlobalAttributes
from mobscript.delayed_instructions import DelayedInstructions
from mobscript.map_controller import MapController

from mobscript.units_controller import UnitsController

from .util.file_operations import create_blank_file

def calculate_dist_between_points(point_1: Tuple[Union[int, float], Union[int, float]], 
                                  point_2: Tuple[Union[int, float], Union[int, float]]) -> float:
    return math.sqrt(((point_1[0] - point_2[0]) ** 2) + ((point_1[1] - point_2[1]) ** 2))


def create_clique_from_nodes(graph: nx.Graph, nodes: List[Hashable]) -> None:
    for current_index in range(len(nodes)):
        for next_index in range(current_index + 1, len(nodes)):
            graph.add_edge(nodes[current_index], nodes[next_index])


def create_satellite_edges(graph: nx.Graph) -> None:
    nodes_with_satellite = [x for x, y in graph.nodes(data=True) if y['has_satellite_link'] == True]
    create_clique_from_nodes(graph, nodes_with_satellite)


def create_cellular_radio_edges(graph: nx.Graph, 
                                cellular_zones: Iterable[Polygon]) -> None:
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


def create_standard_radio_edges(graph: nx.Graph, 
                                standard_radio_radius: Union[int, float]) -> None:
    nodes_with_radios = [x for x, y in graph.nodes(data=True) if y['has_standard_radio'] == True]
    for current_index in range(len(nodes_with_radios)):
        for next_index in range(current_index + 1, len(nodes_with_radios)):
            current_node_key = nodes_with_radios[current_index]
            next_node_key = nodes_with_radios[next_index]
            current_node = graph.nodes[nodes_with_radios[current_index]]
            next_node = graph.nodes[nodes_with_radios[next_index]]
            if calculate_dist_between_points(current_node["coord"], next_node["coord"]) < standard_radio_radius:
                graph.add_edge(current_node_key, next_node_key)


def run_graph_analysis(positions_history: Iterable[Dict[str, Tuple[Union[int, float], Union[int, float]]]], 
                       units_controller: UnitsController, 
                       map_controller: MapController, 
                       global_attributes: GlobalAttributes, 
                       delayed_instructions: DelayedInstructions) -> List[str]:
    graph = nx.Graph()
    for key, value in units_controller.get_units_data().items():
        graph.add_node(key, has_standard_radio=value.has_standard_radio,
                                has_cellular_radio=value.has_cellular_radio,
                                has_satellite_link=value.has_satellite_link)
    
    networks_data = []
    current_time = 0
    for time_frame in positions_history:
        graph = nx.create_empty_copy(graph)

        for key, value in time_frame.items():
            graph.nodes[key]["coord"] = value

        while delayed_instructions.get_change_equip_time() <= current_time:
            instruct = delayed_instructions.get_change_equip_instruct()
            delayed_instructions.pop_change_equip_instruct()
            for unit_key in instruct.key_list:
                if instruct.modify_standard_radio:
                    graph.nodes[unit_key]["has_standard_radio"] = instruct.turn_on
                if instruct.modify_standard_radio:
                    graph.nodes[unit_key]["has_cellular_radio"] = instruct.turn_on
                if instruct.modify_cellular_radio:
                    graph.nodes[unit_key]["has_satellite_link"] = instruct.turn_on

        create_satellite_edges(graph)
        create_cellular_radio_edges(graph, map_controller.get_cellular_zones())
        create_standard_radio_edges(graph, global_attributes.standard_radio_radius)

        # Print serializable graph data
        graph_data = json_graph.node_link_data(graph)
        networks_data.append(json.dumps(graph_data))

        current_time += global_attributes.time_step
    return networks_data


def save_generated_data(file_name: pathlib.Path, networks_data: List[Any]) -> None:
    create_blank_file(file_name)
    with open(file_name, "w") as outfile:
        json.dump(networks_data, outfile, default=lambda o: o.encode(), indent=4)
