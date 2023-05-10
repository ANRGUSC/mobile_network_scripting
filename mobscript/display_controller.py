from typing import Callable, Dict, List, Tuple, Union
import pygame
import math
from pygame.locals import QUIT
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from .data_structures.global_attributes import GlobalAttributes
from .data_structures.unit import Unit
from .map_controller import MapController
from .units_controller import UnitsController
from .log_normal_fading import ShannonCapacity
from .log_normal_fading import CalculateMetrics
from .__init__ import read_json_file
from .__init__ import calculate_dist_between_points
import itertools
import json
import heapq
import matplotlib.pyplot as plt

def distance_point_to_line_segment(point, start, end):
    """Calculate the distance between a point and a line segment."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if dx == dy == 0:  # the segment is just a point
        return math.hypot(point[0] - start[0], point[1] - start[1])

    t = ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / (dx**2 + dy**2)
    t = max(0, min(1, t))  # limit t to the range [0, 1]
    closest_point = start[0] + t * dx, start[1] + t * dy
    return math.hypot(point[0] - closest_point[0], point[1] - closest_point[1])

class UnitSprite():
    def __init__(self, 
                 screen: pygame.Surface, 
                 unit_key: str, 
                 unit_data: Unit, 
                 positions_history, 
                 time_step):
        self.screen = screen
        self.unit_key = unit_key
        self.unit_data = unit_data
        self.positions_history = positions_history
        self.time_step = time_step
        self.radius = 10
        self.curr_pos = None

    def update(self, curr_time: Union[int, float]) -> None:
        time_index = math.floor(curr_time // self.time_step)
        if time_index < len(self.positions_history):
            self.curr_pos = self.positions_history[time_index][self.unit_key]
            self.curr_pos = (self.curr_pos[1], self.curr_pos[0])


    global my_dict
    my_dict = {}

    def display(self,
                convert_coord_func: Callable[[Tuple[int, int], Tuple[int, int], int], Tuple[int, int]],
                origin: Tuple[int, int]) -> None:
        screen_width, screen_height = self.screen.get_size()
       
        converted_coord = convert_coord_func(self.curr_pos, origin, screen_height)
        
        pygame.draw.circle(self.screen, (0, 0, 255), converted_coord, self.radius)
        
        if self.unit_data.has_standard_radio == True:
            my_dict[self.unit_key] = converted_coord
        with open('mobile_network_scripting/mobscript/input_data_defaults/global_attributes.json', 'r') as f:
            data = json.load(f)            
        min_distance = data.get('standard_radio_radius')

        for key1, key2 in itertools.combinations(my_dict.keys(), 2):
            coord1, coord2 = my_dict[key1], my_dict[key2]
            distance = calculate_dist_between_points(coord1, coord2)
            
            if distance < min_distance:
                pygame.draw.line(self.screen, (255, 0, 0), coord1, coord2, width=1)
                mouse_pos = pygame.mouse.get_pos()
                line_start = coord1
                line_end = coord2
                line_thickness = 3
                distance_to_line = distance_point_to_line_segment(mouse_pos, line_start, line_end)

                if distance_to_line < line_thickness:  # Display capacity only if mouse is over the line segment
                    P_t, K, n, d_0, sigma, snr_threshold, bandwidth, packet_size, error_threshold = read_json_file("mobile_network_scripting/examples/overview/inputs.json")
                    capacity = ShannonCapacity()
                    error_prob = CalculateMetrics()
                    capacity.capacity_calculation(P_t, K, n, distance, d_0, sigma, bandwidth)
                    error_prob.bit_error_probability( P_t, snr_threshold, distance ,d_0, K, sigma, bandwidth,n)
            
                    error_prob.packet_error_probability(snr_threshold, error_threshold, packet_size,  P_t, distance ,d_0, K, sigma, bandwidth,n)

                    error_prob.calculate_ETX()
                    details_text = "Shannon Cap: " + str(capacity.shannon_capacity) + ", " + "BER: " + str(error_prob.bit_error_prob) + ", PEP: " + str(error_prob.pep) + ", ETX: " + str(error_prob.etx)

        
                    font = pygame.font.Font(None, 20)
                    details_surface = font.render(details_text, True, (255, 255, 255))
                    text_rect = details_surface.get_rect()
                    background_rect = pygame.Rect(mouse_pos, (text_rect.width + 40, text_rect.height + 30))
                    pygame.draw.rect(self.screen, (0, 0, 0), background_rect)
                    self.screen.blit(details_surface, (mouse_pos[0] + 10, mouse_pos[1] + 10))

        
class DisplayController:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    char_to_image = {}

    def __init__(self, 
                 units_controller: UnitsController, 
                 map_controller: MapController, 
                 positions_history: List[Dict[str, Tuple[Union[int, float], Union[int, float]]]], 
                 global_attributes: GlobalAttributes                 
                 ) -> None:
        self.units_controller = units_controller
        self.map_controller = map_controller
        self.positions_history = positions_history
        self.global_attributes = global_attributes
        self.scale = self.map_controller.get_scale()
        self.length_to_pixels = self.global_attributes.length_to_pixels
        self.multiplier = self.global_attributes.length_to_pixels * self.scale
      
        self.char_to_image['^'] = pygame.image.load("mobile_network_scripting/images/mountain.png")
        self.char_to_image['_'] = pygame.image.load("mobile_network_scripting/images/ground.png")
        self.char_to_image['r'] = pygame.image.load("mobile_network_scripting/images/road.png")

    def convert_coord(self, 
                      coord: Tuple[int, int], 
                      origin: Tuple[int, int], 
                      screen_height: int) -> Tuple[int, int]:
        coord_scaled = tuple(i * self.length_to_pixels for i in coord)
        coord_flip = coord_scaled[0], screen_height - coord_scaled[1]
        coord_by_origin = coord_flip[0] - origin[0], coord_flip[1] + origin[1]
        return coord_by_origin

    def draw_map(self, screen: pygame.Surface, origin: Tuple[int, int]) -> None:
        map = self.map_controller.get_map()
        screen_width, screen_height = screen.get_size()
        font = pygame.font.SysFont('Arial', 10)
        for row in range(0, len(map)):
            for col in range(0, len(map[0])):
                color = (100, 100, 100)
                pos_rect = self.convert_coord((self.scale * col, self.scale * row + self.scale), origin, screen_height)
                pos_char = self.convert_coord((self.scale * col + self.scale / 2, self.scale * row + self.scale / 2),
                                              origin, screen_height)
                rect = [pos_rect[0], pos_rect[1], self.multiplier, self.multiplier]
                curr_char = map[row][col]
                screen.blit(pygame.transform.smoothscale(
                    self.char_to_image[curr_char], (self.multiplier, self.multiplier)), rect)

    def display(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        origin = (0, 0)
        current_time = 0.0
        paused = False
        clock = pygame.time.Clock()

        slider = Slider(screen, 100, 30, self.SCREEN_WIDTH - 310, 20, step=.001, initial=0, min=0, 
            max=self.global_attributes.time_duration)

        def on_button_click():
            nonlocal paused
            paused = not paused
        button = Button(screen, 40, 27, 30, 30, onClick=on_button_click)

        time_duration_text = TextBox(screen, self.SCREEN_WIDTH - 180, 10, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        time_duration_text.setText("Time Duration: {}s".format((self.global_attributes.time_duration)))
        time_duration_text.disable()
        current_time_text = TextBox(screen, self.SCREEN_WIDTH - 180, 35, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        current_time_text.setText("Current Time: {}s".format(current_time))
        current_time_text.disable()

        min_distance = 150

        def on_button_click_calculate_dijkstra():
            nonlocal paused
            paused = not paused
            
            last_positions = {}
            for unit, position in self.positions_history[-1].items():
                last_positions[unit] = position

            last_positions = {node: (pos[0] * 10, pos[1] * 10) for node, pos in last_positions.items()}
            # Define the edges between the nodes
            edges = {}
            for node1, pos1 in last_positions.items():
                edges[node1] = []
                for node2, pos2 in last_positions.items():
                    if node1 != node2:
                        distance = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
                        if distance > min_distance:
                            edges[node1].append((node2, distance))
            

            shortest_path = dijkstra(edges, 'unit_1', 'unit_4')
            fig, ax = plt.subplots(figsize=(8, 8))
            for node, pos in last_positions.items():
                circle = plt.Circle(pos, 15, color=(1, 1, 1), fill=True)
                ax.add_artist(circle)
                plt.text(pos[0], pos[1], node, color=(0, 0, 0), ha='center', va='center', fontsize=10)
                for neighbor, weight in edges[node]:
                    plt.plot([pos[0], last_positions[neighbor][0]], [pos[1], last_positions[neighbor][1]], color=(0, 0, 1), linewidth=2)

            source_node = 'unit_1'
            destination_node = 'unit_4'

            shortest_path = dijkstra(edges, source_node, destination_node)

            for i in range(len(shortest_path) - 1):
                node_1 = shortest_path[i]
                node_2 = shortest_path[i+1]
                pos_1 = last_positions[node_1]
                pos_2 = last_positions[node_2]
                plt.plot([pos_1[0], pos_2[0]], [pos_1[1], pos_2[1]], color=(0, 1, 0), linewidth=3)
                plt.plot(pos_1[0], pos_1[1], 'o', color=(0, 1, 0), markersize=10)
                plt.plot(pos_2[0], pos_2[1], 'o', color=(0, 1, 0), markersize=10)

            plt.title(f'Shortest path from {source_node} to {destination_node}')
            plt.axis('equal')
            plt.show()

        button_path = Button(screen, 100, 100, 30, 30, onClick=on_button_click_calculate_dijkstra)        
        button_det = TextBox(screen, self.SCREEN_WIDTH - 650, 100, 180, 30,
                            fontSize=24, borderThickness=0, backgroundColor=(0, 0, 0, 0))
        button_det.setText("Dijkstra's Path")
        button_det.disable()

        # Define the Dijkstra's shortest path algorithm
        def dijkstra(graph, start, end):
            dist = {node: math.inf for node in graph}
            dist[start] = 0
            heap = [(0, start)]
            path = {}

            while heap:
                (current_dist, current_node) = heapq.heappop(heap)

                if current_node == end:
                    break

                for (neighbor, weight) in graph[current_node]:
                    distance = current_dist + weight
                    
                    if distance < dist[neighbor]:
                        dist[neighbor] = distance
                        heapq.heappush(heap, (distance, neighbor))
                        if(distance > min_distance):
                            path[neighbor] = current_node

            shortest_path = [end]
            while end != start:
                shortest_path.append(path.get(end))
                end = path.get(end)
            shortest_path.reverse()

            return shortest_path

        instructions_text_1 = TextBox(screen, self.SCREEN_WIDTH - 180, 80, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        instructions_text_1.setText("i - Toggle Instructions")
        instructions_text_1.disable()

        instructions_text_2 = TextBox(screen, self.SCREEN_WIDTH - 180, 105, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        instructions_text_2.setText("arrows - Move screen")
        instructions_text_2.disable()

        instructions_text_3 = TextBox(screen, self.SCREEN_WIDTH - 180, 130, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        instructions_text_3.setText("space - toggle pause")
        instructions_text_3.disable()

        unit_sprites = {}
        units_data = self.units_controller.get_units_data()
        for unit_key in units_data:
            unit_sprites[unit_key] = UnitSprite(
                screen, 
                unit_key, 
                units_data[unit_key],
                self.positions_history, 
                self.global_attributes.time_step
            )

        display_on = True
        display_instructions = True
        slider_changed = False
        while display_on:
            current_time_text.setText("Current Time: {:.0f}s".format(current_time))
            clock.tick()
            time_progression = clock.get_time() / 1000
            slider_time = slider.getValue()

            if not paused and abs(slider_time - current_time) < .0001 and current_time < self.global_attributes.time_duration:
                current_time = current_time + time_progression
                slider.setValue(current_time)
                slider_changed = False
            else:
                if current_time != slider_time:
                    slider_changed = True
                current_time = slider_time            

            screen.fill((255, 255, 255))
            self.draw_map(screen, origin)
            for unit_sprite in unit_sprites.values():
                if not paused or slider_changed:
                    unit_sprite.update(current_time)
                unit_sprite.display(self.convert_coord, origin)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    display_on = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        origin = origin[0] + self.multiplier, origin[1]
                    if event.key == pygame.K_RIGHT:
                        origin = origin[0] - self.multiplier, origin[1]
                    if event.key == pygame.K_UP:
                        origin = origin[0], origin[1] - self.multiplier
                    if event.key == pygame.K_DOWN:
                        origin = origin[0], origin[1] + self.multiplier
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                    if event.key == pygame.K_i:
                        if display_instructions == True:
                            display_instructions = False
                            instructions_text_1.hide()
                            instructions_text_2.hide()
                            instructions_text_3.hide()
                        else:
                            display_instructions = True
                            instructions_text_1.show()
                            instructions_text_2.show()
                            instructions_text_3.show()
            pygame_widgets.update(events)
            mouse_pos = pygame.mouse.get_pos()
            pygame.display.flip()