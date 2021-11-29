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

    def display(self, 
                convert_coord_func: Callable[[Tuple[int, int], Tuple[int, int], int], Tuple[int, int]], 
                origin: Tuple[int, int]) -> None:
        screen_width, screen_height = self.screen.get_size()
        converted_coord = convert_coord_func(self.curr_pos, origin, screen_height)
        pygame.draw.circle(self.screen, (0, 0, 255), converted_coord, self.radius)


class DisplayController:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    char_to_image = {}

    def __init__(self, 
                 units_controller: UnitsController, 
                 map_controller: MapController, 
                 positions_history: List[Dict[str, Tuple[Union[int, float], Union[int, float]]]], 
                 global_attributes: GlobalAttributes) -> None:
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
                # pygame.draw.rect(screen, color, [pos_rect[0], pos_rect[1], self.multiplier, self.multiplier])
                rect = [pos_rect[0], pos_rect[1], self.multiplier, self.multiplier]
                curr_char = map[row][col]
                screen.blit(pygame.transform.smoothscale(
                    self.char_to_image[curr_char], (self.multiplier, self.multiplier)), rect)
                # screen.blit(font.render(map[row][col], True, (255, 0, 0)), pos_char)

    def display(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        origin = (0, 0)
        current_time = 0.0
        paused = False
        clock = pygame.time.Clock()

        slider = Slider(screen, 100, 30, self.SCREEN_WIDTH - 310, 20, step=.001, initial=0, min=0, 
            max=self.global_attributes.time_duration)
        button = Button(screen, 40, 27, 30, 30,
            onClick=lambda: (paused := not paused))

        time_duration_text = TextBox(screen, self.SCREEN_WIDTH - 180, 10, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        time_duration_text.setText("Time Duration: {}s".format((self.global_attributes.time_duration)))
        time_duration_text.disable()
        current_time_text = TextBox(screen, self.SCREEN_WIDTH - 180, 35, 180, 30,
            fontSize=24, borderThickness=0, textColour=(50, 50, 50))
        current_time_text.setText("Current Time: {}s".format(current_time))
        current_time_text.disable()

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
            pygame.display.flip()