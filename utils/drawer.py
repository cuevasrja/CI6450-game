import math
from typing import List, Tuple
import pygame

from utils.physics import Kinematic

def draw_polygon(screen: pygame.Surface, color: str, position: pygame.Vector2, orientation: float, size: int = 20) -> None:
    pygame.draw.polygon(screen, color, [
        (position.x + math.cos(orientation) * size, position.y + math.sin(orientation) * size), 
        (position.x + math.cos(orientation + 2.5) * size, position.y + math.sin(orientation + 2.5) * size), 
        (position.x + math.cos(orientation - 2.5) * size, position.y + math.sin(orientation - 2.5) * size)
    ])

def draw_polygon_by_class(screen: pygame.Surface, color: str, player: Kinematic) -> None:
    draw_polygon(screen, color, player.position, player.orientation)
