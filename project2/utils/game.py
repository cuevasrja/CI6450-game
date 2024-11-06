import math
from typing import Dict, List
import pygame
from utils.a_star import pathfind_astar
from utils.connection import Connection
from utils.game_graph import GameGraph
from utils.manhattan_heuristic import ManhattanHeuristic

def check_collision(zoomed_world: pygame.Surface, x: float, y: float) -> bool:
    """
    ### Description
    Check if there is a collision at the given position in the zoomed world.

    ### Parameters
    - zoomed_world: The zoomed world surface.
    - x: The x coordinate.
    - y: The y coordinate.

    ### Returns
    - True if there is a collision, False otherwise.
    """
    try:
        color = zoomed_world.get_at((int(x), int(y)))
        # rgb(134, 101, 156)
        return 0 < color[0] and 0 < color[1] and 0 < color[2]
    except IndexError:
        return True  # Out of bounds

def is_valid_position(zoomed_world: pygame.Surface, x: int, y: int) -> bool:
    """
    ### Description
    Check if the given position is valid in the zoomed world.

    ### Parameters
    - zoomed_world: The zoomed world surface.
    - x: The x coordinate.
    - y: The y coordinate.

    ### Returns
    - True if the position is valid, False otherwise.
    """
    return not check_collision(zoomed_world, x, y)

# Función para obtener el camino entre dos puntos
def get_path(game_graph: GameGraph, block_size: int, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Connection]:
    """
    ### Description
    Get the path between two points using the A* algorithm.

    ### Parameters
    - game_graph: The game graph.
    - block_size: The size of a block.
    - start_x: The x coordinate of the start point.
    - start_y: The y coordinate of the start point.
    - end_x: The x coordinate of the end point.
    - end_y: The y coordinate of the end point.

    ### Returns
    - The path between the two points
    """
    start_node = game_graph.nodes.get((start_x // block_size, start_y // block_size))
    end_node = game_graph.nodes.get((end_x // block_size, end_y // block_size))
    
    if start_node and end_node:
        heuristic = ManhattanHeuristic(end_node)
        path = pathfind_astar(game_graph, start_node, end_node, heuristic)
        return path
    return None

# Movement zone for enemy 1
ENEMY_MIN_X = 850
ENEMY_MAX_X = 1150
DETECTION_RADIUS = 150

def test_player_in_range_and_zone(enemy_pos: pygame.Vector2, player_pos: pygame.Vector2) -> bool:
    """
    ### Description
    Check if the player is in the detection range and movement zone of the enemy.

    ### Parameters
    - enemy_pos: The position of the enemy.
    - player_pos: The position of the player.

    ### Returns
    - True if the player is in the detection range and movement zone of the enemy, False otherwise.
    """
    dx: int = player_pos[0] - enemy_pos[0]
    dy: int = player_pos[1] - enemy_pos[1]
    distance: float = math.sqrt(dx*dx + dy*dy)
    
    # Check if player is in detection range
    in_range: bool = distance <= DETECTION_RADIUS
    
    # Expand the movement zone when pursuing player
    if in_range:
        # Wider zone when chasing
        in_zone = ENEMY_MIN_X - 100 <= enemy_pos[0] <= ENEMY_MAX_X + 100
    else:
        # Normal patrol zone
        in_zone = ENEMY_MIN_X <= enemy_pos[0] <= ENEMY_MAX_X
    
    return in_range and in_zone

def find_nearest_enemy(game_graph: GameGraph, block_size: int, player_x: int, player_y: int, enemy_positions: List[Dict[str, int|pygame.Surface]]) -> List[Connection]:
    """
    ### Description
    Find the nearest enemy to the player.

    ### Parameters
    - game_graph: The game graph.
    - block_size: The size of a block.
    - player_x: The x coordinate of the player.
    - player_y: The y coordinate of the player.
    - enemy_positions: The positions of the enemies.

    ### Returns
    - The path to the nearest enemy and the target enemy.
    """
    best_distance: float = float('inf')
    best_route: List[Connection] = None
    target_enemy = None

    for enemy in enemy_positions:
        path_to_enemy = get_path(game_graph, block_size, player_x, player_y, enemy["x"], enemy["y"])
        if path_to_enemy:
            # Calculate distance to enemy
            distance = len(path_to_enemy)
            if distance < best_distance:
                best_distance = distance
                best_route = path_to_enemy
                target_enemy = enemy

    return best_route, target_enemy

def draw_path(screen: pygame.Surface, path: List[Connection], camera_x: int, camera_y: int, block_size: int) -> None:
    """
    ### Description
    Draw the path on the screen.

    ### Parameters
    - screen: The screen surface.
    - path: The path to draw.
    - camera_x: The x coordinate of the camera.
    - camera_y: The y coordinate of the camera.
    - block_size: The size of a block.

    ### Returns
    - None
    """
    if path:
        # Draw path nodes
        for i in range(len(path)-1):
            start = path[i].from_node
            end = path[i].to_node
            
            start_pos = (start.x * block_size - camera_x, 
                        start.y * block_size - camera_y)
            end_pos = (end.x * block_size - camera_x,
                      end.y * block_size - camera_y)
            
            pygame.draw.line(screen, (255,0,0), start_pos, end_pos, 2)

def check_experiment_collision(player_pos: pygame.Vector2, exp_pos: pygame.Vector2, threshold: int = 30) -> bool:
    """
    ### Description
    Check if the player is close to the experiment.

    ### Parameters
    - player_pos: The position of the player.
    - exp_pos: The position of the experiment.
    - threshold: The distance threshold.

    ### Returns
    - True if the player is close to the experiment, False otherwise.
    """
    dx: int = player_pos[0] - exp_pos["x"]
    dy: int = player_pos[1] - exp_pos["y"]
    collision_distance: float = (dx**2 + dy**2)**0.5
    return collision_distance < threshold