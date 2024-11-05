import math
from typing import List
import pygame
from utils.a_star import pathfind_astar
from utils.connection import Connection
from utils.game_graph import GameGraph
from utils.manhattan_heuristic import ManhattanHeuristic

def check_collision(zoomed_world: pygame.Surface, x: float, y: float):
    # Obtener el color del píxel en la posición del jugador
    try:
        color = zoomed_world.get_at((int(x), int(y)))
        # rgb(134, 101, 156)
        return 0 < color[0] and 0 < color[1] and 0 < color[2]
    except IndexError:
        return True  # Si está fuera de los límites, consideramos que hay colisión

# Función para validar la posición del jugador
def is_valid_position(zoomed_world: pygame.Surface, x: int, y: int) -> bool:
    return not check_collision(zoomed_world, x, y)

# Función para obtener el camino entre dos puntos
def get_path(game_graph: GameGraph, block_size: int, start_x: int, start_y: int, end_x: int, end_y: int):
    start_node = game_graph.nodes.get((start_x // block_size, start_y // block_size))
    end_node = game_graph.nodes.get((end_x // block_size, end_y // block_size))
    
    if start_node and end_node:
        heuristic = ManhattanHeuristic(end_node)
        path = pathfind_astar(game_graph, start_node, end_node, heuristic)
        return path
    return None

# Zona de movimiento del experimento 1
EXP1_MIN_X = 850
EXP1_MAX_X = 1150
DETECTION_RADIUS = 150

# Función para el árbol de decisión
def test_player_in_range_and_zone(enemy_pos: pygame.Vector2, player_pos: pygame.Vector2):
    dx: int = player_pos[0] - enemy_pos[0]
    dy: int = player_pos[1] - enemy_pos[1]
    distance: float = math.sqrt(dx*dx + dy*dy)
    
    # Check if player is in detection range
    in_range: bool = distance <= DETECTION_RADIUS
    
    # Expand the movement zone when pursuing player
    if in_range:
        # Wider zone when chasing
        in_zone = EXP1_MIN_X - 100 <= enemy_pos[0] <= EXP1_MAX_X + 100
    else:
        # Normal patrol zone
        in_zone = EXP1_MIN_X <= enemy_pos[0] <= EXP1_MAX_X
    
    return in_range and in_zone

# Función para encontrar el experimento más cercano
def find_nearest_enemy(game_graph: GameGraph, block_size: int, player_x, player_y, enemy_positions):
    mejor_distancia = float('inf')
    mejor_camino = None
    experimento_objetivo = None

    for enemy in enemy_positions:
        camino = get_path(game_graph, block_size, player_x, player_y, enemy["x"], enemy["y"])
        if camino:
            # Calculamos la longitud del camino
            distancia = len(camino)
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_camino = camino
                experimento_objetivo = enemy

    return mejor_camino, experimento_objetivo

# Función para dibujar el camino
def draw_path(screen: pygame.Surface, path: List[Connection], camera_x: int, camera_y: int, block_size: int):
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

# Función para detectar colisión con los experimentos
def check_experiment_collision(player_pos: pygame.Vector2, exp_pos: pygame.Vector2, threshold: int = 30):
    dx: int = player_pos[0] - exp_pos["x"]
    dy: int = player_pos[1] - exp_pos["y"]
    collision_distance: float = (dx**2 + dy**2)**0.5
    return collision_distance < threshold