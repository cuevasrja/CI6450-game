from typing import Dict, List, Tuple
import pygame
from utils.node import Node, TileNode
from utils.graph import Graph

class GameGraph(Graph):
    """
    ### Description
    A graph representing a game world.

    ### Attributes
    - `surface`: The surface representing the game world.
    - `block_size`: The size of each tile in the game world.
    - `nodes`: A dictionary mapping tile coordinates to nodes.

    ### Methods
    - `build_graph()`: Creates a graph from the game world.
    - `is_wall(x: int, y: int) -> bool`: Returns whether a tile is a wall.
    - `add_connections_for_tile(x: int, y: int)`: Adds connections for a tile.
    - `draw_world_representation(surface: pygame.Surface, camera_x: int, camera_y: int)`: Draws the world representation.

    """
    def __init__(self, surface: pygame.Surface, block_size: int = 32):
        super().__init__()
        self.block_size: int = block_size
        self.surface: pygame.Surface = surface
        self.nodes: Dict[pygame.Vector2, TileNode] = {}
        self.build_graph()
    
    def build_graph(self):
        width: int = self.surface.get_width() // self.block_size
        height: int = self.surface.get_height() // self.block_size
        
        # Create nodes for walkable tiles
        for y in range(height):
            for x in range(width):
                if not self.is_wall(x, y):
                    node: TileNode = TileNode(x, y)
                    self.nodes[(x, y)] = node
                    
        # Create connections between adjacent walkable tiles
        for y in range(height):
            for x in range(width):
                if (x, y) in self.nodes:
                    self.add_connections_for_tile(x, y)
    
    def is_wall(self, x: int, y: int) -> bool:
        pixel_x: int = x * self.block_size + self.block_size // 2
        pixel_y: int = y * self.block_size + self.block_size // 2
        try:
            color: List[int] = self.surface.get_at((pixel_x, pixel_y))
            return 0 < color[0] and 0 < color[1] and 0 < color[2]
        except IndexError:
            return True
    
    def add_connections_for_tile(self, x: int, y: int):
        directions: List[Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # N, E, S, W
        current_node = self.nodes[(x, y)]
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in self.nodes:
                neighbor_node: TileNode = self.nodes[(new_x, new_y)]
                self.add_connection(current_node, neighbor_node, 1.0)
    
    def draw_world_representation(self, surface: pygame.Surface, camera_x: int, camera_y: int):
        # Dibuja la cuadrícula
        for (x, y), node in self.nodes.items():
            screen_x = x * self.block_size - camera_x
            screen_y = y * self.block_size - camera_y
            
            # Dibuja el borde de cada tile
            pygame.draw.rect(surface, (0, 255, 0), 
                            (screen_x, screen_y, self.block_size, self.block_size), 1)
            
            # Dibuja el nodo representativo (punto central)
            pygame.draw.circle(surface, (255, 0, 0),
                            (screen_x + self.block_size//2, screen_y + self.block_size//2), 3)
            
            # Dibuja las conexiones
            for connection in self.get_connections(node):
                to_node: Node|TileNode = connection.get_to_node()
                if isinstance(to_node, TileNode):
                    end_x = to_node.x * self.block_size - camera_x + self.block_size//2
                    end_y = to_node.y * self.block_size - camera_y + self.block_size//2
                    pygame.draw.line(surface, (0, 0, 255),
                                (screen_x + self.block_size//2, screen_y + self.block_size//2),
                                (end_x, end_y), 1)