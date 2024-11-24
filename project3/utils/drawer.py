import math
import pygame
from utils.kinematic import Kinematic

def draw_polygon(screen: pygame.Surface, color: str, position: pygame.Vector2, orientation: float, size: int = 20) -> None:
    """
    ### Description
    Draws a triangle on the screen.

    ### Parameters
    - screen: pygame.Surface - The screen to draw on.
    - color: str - The color of the triangle.
    - position: pygame.Vector2 - The position of the triangle.
    - orientation: float - The orientation of the triangle.
    - size: int - The size of the triangle. (Default is 20)

    ### Returns
    - None
    """
    pygame.draw.polygon(screen, color, [
        (position.x + math.cos(orientation) * size, position.y + math.sin(orientation) * size), 
        (position.x + math.cos(orientation + 2.5) * size, position.y + math.sin(orientation + 2.5) * size), 
        (position.x + math.cos(orientation - 2.5) * size, position.y + math.sin(orientation - 2.5) * size)
    ])

def draw_polygon_by_class(screen: pygame.Surface, color: str, player: Kinematic, camera: pygame.Vector2) -> None:
    """
    ### Description
    Draws a triangle on the screen using a Kinematic object.

    ### Parameters
    - screen: pygame.Surface - The screen to draw on.
    - color: str - The color of the triangle.
    - player: Kinematic - The player object.

    ### Returns
    - None
    """
    draw_polygon(screen, color, player.position - camera, player.orientation)