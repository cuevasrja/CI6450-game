import math
from typing import Dict, List, Tuple
import pygame
from utils.kinematic import Kinematic
from utils.a_star import pathfind_astar
from utils.tactical_a_star import pathfind_tactical_astar
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

def get_path_and_evade(game_graph: GameGraph, block_size: int, start: pygame.Vector2, end: pygame.Vector2, player: pygame.Vector2) -> List[Connection]:
    """
    ### Description
    Get the path between two points using the A* algorithm and evade the enemies.

    ### Parameters
    - game_graph: The game graph.
    - block_size: The size of a block.
    - start: The start point.
    - end: The end point.
    - player: The player's position that the enemy should evade.

    ### Returns
    - The path between the two points
    """
    start_node = game_graph.nodes.get((start.x // block_size, start.y // block_size))
    end_node = game_graph.nodes.get((end.x // block_size, end.y // block_size))

    player_node = game_graph.nodes.get((player.x // block_size, player.y // block_size))
    
    if start_node and end_node:
        heuristic = ManhattanHeuristic(end_node)
        path = pathfind_tactical_astar(game_graph, start_node, end_node, heuristic, player_node)
        return path
    return

# Movement zone for enemy 1
ENEMY_MIN_X = 800
ENEMY_MAX_X = 1300
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

def find_nearest_enemy(game_graph: GameGraph, block_size: int, player: pygame.Vector2, enemy_positions: List[pygame.Vector2]) -> List[Connection]:
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
        if enemy is None:
            continue
        path_to_enemy = get_path(game_graph, block_size, player.x, player.y, enemy.x, enemy.y)
        if path_to_enemy:
            # Calculate distance to enemy
            distance = len(path_to_enemy)
            if distance < best_distance:
                best_distance = distance
                best_route = path_to_enemy
                target_enemy = enemy

    return best_route, target_enemy

def find_nearest_target_and_evade_obstacles(game_graph: GameGraph, block_size: int, player: pygame.Vector2, blackhole_positions: List[Dict[str, int|pygame.Surface]], enemy: pygame.Vector2) -> List[Connection]:
    """
    ### Description
    Find the nearest blackhole to the player and evade the player.

    ### Parameters
    - game_graph: The game graph.
    - block_size: The size of a block.
    - player: The player's position.
    - blackhole_positions: The positions of the blackholes.
    - enemy: The enemy's position.

    ### Returns
    - The path to the nearest blackhole and the target blackhole.
    """
    best_distance: float = float('inf')
    best_route: List[Connection] = None
    target_blackhole = None

    for blackhole in blackhole_positions:
        if blackhole is None:
            continue
        path_to_blackhole = get_path_and_evade(game_graph, block_size, player, blackhole, enemy)
        if path_to_blackhole:
            # Calculate distance to blackhole
            distance = len(path_to_blackhole)
            if distance < best_distance:
                best_distance = distance
                best_route = path_to_blackhole
                target_blackhole = blackhole

    return best_route, target_blackhole

def draw_path(screen: pygame.Surface, path: List[Connection], camera_x: int, camera_y: int, block_size: int, color: Tuple[int, int, int]|str = (255, 0, 0)) -> None:
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
            
            pygame.draw.line(screen, color, start_pos, end_pos, 2)

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

def key_checker(keys: pygame.key.ScancodeWrapper, player: Kinematic, hist_pos: pygame.Vector2, const_velocity: float, dt: float, zoomed_world) -> None:
    """
    ### Description
    Checks the keys pressed by the user.

    ### Parameters
    - keys: pygame.key.ScancodeWrapper : The keys pressed by the user.
    - player: Kinematic : The player to move.
    - hist_pos: pygame.Vector2 : The position of the player.
    - const_velocity: float : The velocity of the player.
    - dt: float : The time elapsed.

    ### Returns
    - None
    """

    # If the user presses the key, the player moves
    
    distance = pygame.Vector2(0, 0)
    velocity = player.get_velocity()
    FPS = 1 / dt if dt != 0 else 1

    # Key D. Right
    if keys[pygame.K_d]:
        distance += pygame.Vector2(const_velocity * dt, 0)
        hist_pos.x += const_velocity * dt
        velocity.x = const_velocity * FPS

    # Key W. Up
    if keys[pygame.K_w]:
        distance += pygame.Vector2(0, -const_velocity * dt)
        hist_pos.y -= const_velocity * dt
        velocity.y = -const_velocity * FPS

    # Key A. Left
    if keys[pygame.K_a]:
        distance += pygame.Vector2(-const_velocity * dt, 0)
        hist_pos.x -= const_velocity * dt
        velocity.x = -const_velocity * FPS
    
    # Key S. Down
    if keys[pygame.K_s]:
        distance += pygame.Vector2(0, const_velocity * dt)
        hist_pos.y += const_velocity * dt
        velocity.y = const_velocity * FPS

    if not check_collision(zoomed_world, player.get_x() + distance.x, player.get_y() + distance.y):
        player.set_velocity(velocity.x, velocity.y)
        player.add_position(distance.x, distance.y)

    # If the user releases the key or does not press another key, the player stops
    if not(keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_q]):
        player.set_velocity(x=0, y=0)