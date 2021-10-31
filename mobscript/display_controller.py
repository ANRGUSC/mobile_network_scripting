from typing import Callable, Dict, List, Tuple, Union
import pygame
import math
from pygame.locals import QUIT
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
        self.curr_pos = self.positions_history[time_index][self.unit_key]
        self.curr_pos = (self.curr_pos[1], self.curr_pos[0])

    def display(self, 
                convert_coord_func: Callable[[Tuple[int, int], Tuple[int, int], int], Tuple[int, int]], 
                origin: Tuple[int, int]) -> None:
        screen_width, screen_height = self.screen.get_size()
        converted_coord = convert_coord_func(self.curr_pos, origin, screen_height)
        pygame.draw.circle(self.screen, (0, 0, 255), converted_coord, self.radius)
        # pygame.draw.rect(self.screen, (0, 0, 255), [converted_coord[0], converted_coord[1], 50, 50])


class DisplayController:
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
                pygame.draw.rect(screen, color, [pos_rect[0], pos_rect[1], self.multiplier, self.multiplier])
                screen.blit(font.render(map[row][col], True, (255, 0, 0)), pos_char)

    def display(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        origin = (0, 0)

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

        start_time = pygame.time.get_ticks()

        display_on = True
        while display_on:
            frame_time = pygame.time.get_ticks()
            screen.fill((255, 255, 255))
            self.draw_map(screen, origin)
            for unit_sprite in unit_sprites.values():
                unit_sprite.update((frame_time - start_time) / 1000.0)
                unit_sprite.display(self.convert_coord, origin)

            for event in pygame.event.get():
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
            pygame.display.flip()
