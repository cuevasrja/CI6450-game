import pygame, sys
from utils.game import check_collision, draw_path, find_nearest_enemy, test_player_in_range_and_zone
from utils.game_graph import GameGraph
from utils.kinematic_arrive import KinematicArrive
from utils.kinematic_arrive_descision import KinematicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision
from pygame.locals import *

# Inicialización del motor de juego
pygame.init()

# Se crea la ventana
window_width, window_height = 700, 600
SCREEN = pygame.display.set_mode((window_width,window_height))

# Nombre de la ventana
pygame.display.set_caption("Space Invaders")

# Fondo
background_image = pygame.image.load("./imgs/background.jpg").convert()

# Factor de zoom
ZOOM = 1.50

# Ajustar el tamaño del laberinto con el zoom
zoomed_world = pygame.transform.scale(
    background_image, 
    (int(background_image.get_width() * ZOOM), 
     int(background_image.get_height() * ZOOM))
)

# Inicialización de la ventana
SCREEN.blit(background_image, (0,0))

# Usaremos la representación Tile Graph para representar el laberinto
block_size = 40
game_graph = GameGraph(zoomed_world, block_size)

# Posición de la cámara
camera_x = 0
camera_y = 0

# PERSONAJES
# Cargamos las imágenes del jugador
standing_player = pygame.image.load("./imgs/player_r.png")
player_standing_left = pygame.image.load("./imgs/player_l.png")

# Movimiento del jugador
player_movement_right = [pygame.image.load(f"./imgs/player_r.png") for i in range(1, 7)]
player_movement_left = [pygame.image.load(f"./imgs/player_l.png") for i in range(1, 7)]
player_movement_up = [pygame.image.load(f"./imgs/player_t.png") for i in range(1, 7)]
player_movement_down = [pygame.image.load(f"./imgs/player_b.png") for i in range(1, 7)]

steps = 0
direction = 'right'
    
# Cargamos las imágenes de los enemigos
experimento1 = pygame.image.load("./imgs/enemy.png")
experimento2 = pygame.image.load("./imgs/enemy.png")

# Movimiento del experimento 1
enemyMove1Right = [pygame.image.load(f"./imgs/enemy_r.png") for i in range(1, 6)]
enemy1MoveLeft = [pygame.image.load(f"./imgs/enemy_l.png") for i in range(1, 6)]

enemy1AttackRight = [pygame.image.load(f"./imgs/enemy_r.png") for i in range(1, 5)]
attackExperiment1Left = [pygame.image.load(f"./imgs/enemy_l.png") for i in range(1, 5)]

# Movimiento del experimento 2
enemy2MoveRight = [pygame.image.load(f"./imgs/enemy_r.png") for i in range(1, 7)]
enemy2MoveLeft = [pygame.image.load(f"./imgs/enemy_l.png") for i in range(1, 7)]

# Variables para el movimiento de los enemigos
ENEMY_SPEED = 10
enemy_directions = ['right', 'right']
enemy_animation_counters = [0, 0]

# Obstáculos
obs = pygame.image.load("./imgs/obstacle.png")

# Secuencia de explosion
explosion = [pygame.image.load(f"./imgs/obstacle.png") for i in range(1, 13)]

PLAYER_SCALE = 1.5
scaled_player = pygame.transform.scale(
    standing_player,
    (int(standing_player.get_width() * PLAYER_SCALE),
     int(standing_player.get_height() * PLAYER_SCALE))
)

# Después de cargar las imágenes, agregar escalado para enemigos y bombas
ENEMY_SCALE = 1.2
BOMB_SCALE = 1.5

scaled_enemy_experiment1 = pygame.transform.scale(
    experimento1,
    (int(experimento1.get_width() * ENEMY_SCALE),
     int(experimento1.get_height() * ENEMY_SCALE))
)

scaled_enemy_experiment2 = pygame.transform.scale(
    experimento2,
    (int(experimento2.get_width() * ENEMY_SCALE),
     int(experimento2.get_height() * ENEMY_SCALE))
)

scaled_obstacle_bomb = pygame.transform.scale(
    obs,
    (int(obs.get_width() * BOMB_SCALE),
     int(obs.get_height() * BOMB_SCALE))
)

# Posiciones actualizadas para los enemigos
enemy_positions = [
    {"x": 1000, "y": 650, "sprite": scaled_enemy_experiment1, "sprites_right": enemyMove1Right, "sprites_left": enemy1MoveLeft, "is_attacking": False},
    {"x": 1300, "y": 200, "sprite": scaled_enemy_experiment2, "sprites_right": enemy2MoveRight, "sprites_left": enemy2MoveLeft, "is_attacking": False}
]

# Posiciones actualizadas para las bombas
bomb_positions = [
    {"x": 900, "y": 1200},  # Primera bomba
    {"x": 1650, "y": 600},  # Segunda bomba
    {"x": 1075, "y": 450},  # Tercera bomba
    {"x": 500, "y": 200}   # Cuarta bomba
]

# Crear una máscara del laberinto para colisiones
maze_mask = pygame.mask.from_surface(zoomed_world)

# Posición del jugador en el mundo
player_x = 0
player_y = 700 

# Límites del mundo
WORLD_WIDTH = zoomed_world.get_width()
WORLD_HEIGHT = zoomed_world.get_height()

# Control de FPS
reloj = pygame.time.Clock()

# Márgenes para activar el movimiento de la cámara
CAMERA_MARGIN = 200
MOVE_SPEED = 10

# Acciones del experimento 1
# Perseguir al jugador

ARRIVAL_RADIUS = 30
MAX_SPEED = 10

# Variables for pathfinding
current_path = None
target_exp = None
current_sprite = standing_player

# BUCLE DE JUEGO
while True:
    # FPS
    reloj.tick(60)
    
    # Bucle del juego
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    # Guardar posición anterior
    old_x = player_x
    old_y = player_y
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    new_x = player_x
    new_y = player_y

    # Then modify your game loop where you handle player movement:
    animacion_velocidad = 0.5
    
    if keys[pygame.K_a]:
        new_x -= MOVE_SPEED
        direction = 'left'
        steps += animacion_velocidad
        if steps >= len(player_movement_left):
            steps = 0
        current_sprite = player_movement_left[int(steps)]
    elif keys[pygame.K_d]:
        new_x += MOVE_SPEED
        direction = 'right'
        steps += animacion_velocidad
        if steps >= len(player_movement_right):
            steps = 0
        current_sprite = player_movement_right[int(steps)]
    elif keys[pygame.K_w]:
        new_y -= MOVE_SPEED
        steps += animacion_velocidad
        if steps >= len(player_movement_up):
            steps = 0
        current_sprite = player_movement_up[int(steps)]
    elif keys[pygame.K_s]:
        new_y += MOVE_SPEED
        steps += animacion_velocidad
        if steps >= len(player_movement_down):
            steps = 0
        current_sprite = player_movement_down[int(steps)]
    elif keys[pygame.K_SPACE]:
        # Get path to nearest experiment
        current_path, target_exp = find_nearest_enemy(game_graph, block_size, player_x, player_y, enemy_positions)
    
        if current_path:
            # Move player along path
            next_node = current_path[0].to_node
            target_x = next_node.x * block_size
            target_y = next_node.y * block_size
            
            # Calculate movement direction
            dx = target_x - player_x
            dy = target_y - player_y
            dist = ((dx**2 + dy**2)**0.5)
            
            if dist > 0:
                # Normalize and apply movement
                dx = dx/dist * MOVE_SPEED  
                dy = dy/dist * MOVE_SPEED
                
                new_x = player_x + dx
                new_y = player_y + dy
                
                if not check_collision(zoomed_world, new_x, new_y):
                    player_x = new_x
                    player_y = new_y
            
            # Draw path
            draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    else:
        steps = 0
        current_sprite = standing_player if direction == 'right' else player_standing_left

    # Scale the current sprite
    scaled_current_sprite = pygame.transform.scale(
        current_sprite,
        (int(current_sprite.get_width() * PLAYER_SCALE),
         int(current_sprite.get_height() * PLAYER_SCALE))
    )

    # Verificar colisiones antes de actualizar la posición
    if not check_collision(zoomed_world, new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    # Limitar al jugador dentro del mundo
    player_x = max(scaled_player.get_width()//2, min(WORLD_WIDTH - scaled_player.get_width()//2, player_x))
    player_y = max(scaled_player.get_height()//2, min(WORLD_HEIGHT - scaled_player.get_height()//2, player_y))
    
    # Actualizar la cámara
    player_screen_x = player_x - camera_x
    player_screen_y = player_y - camera_y
    
    if player_screen_x > window_width - CAMERA_MARGIN:
        camera_x += player_screen_x - (window_width - CAMERA_MARGIN)
    elif player_screen_x < CAMERA_MARGIN:
        camera_x += player_screen_x - CAMERA_MARGIN
        
    if player_screen_y > window_height - CAMERA_MARGIN:
        camera_y += player_screen_y - (window_height - CAMERA_MARGIN)
    elif player_screen_y < CAMERA_MARGIN:
        camera_y += player_screen_y - CAMERA_MARGIN
    
    camera_x = max(0, min(camera_x, WORLD_WIDTH - window_width))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - window_height))
    
    # Dibujar
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(zoomed_world, (-camera_x, -camera_y))
    
    # Agregar esta línea para dibujar la representación del mundo
    game_graph.draw_world_representation(SCREEN, camera_x, camera_y)
    
    # Replace the drawing of scaled_player with scaled_current_sprite
    SCREEN.blit(scaled_current_sprite, (player_x - camera_x - scaled_current_sprite.get_width()//2, 
                                         player_y - camera_y - scaled_current_sprite.get_height()//2))
    
    # Actualizar posición y animación de los enemigos
    for i, enemy in enumerate(enemy_positions):
        if i == 0:  # Solo para el experimento 1# Construir el árbol de decisión
            kinematic_action = KinematicArriveAction(enemy, (player_x, player_y), MAX_SPEED, ARRIVAL_RADIUS)
            patrol_action = PatrolAction(enemy, enemy_directions[i])
            
            chase_decision = InRangeDecision(
                (enemy["x"], enemy["y"]),
                (player_x, player_y),
                kinematic_action,
                patrol_action,
                test_player_in_range_and_zone
            )
            
            attack_action = AttackAction(enemy, enemy_directions[i], enemy1AttackRight, attackExperiment1Left)
            attack_decision = PlayerReachedDecision(
                (enemy["x"], enemy["y"]),
                (player_x, player_y),
                attack_action,
                chase_decision,
                ARRIVAL_RADIUS
            )
            
            action = attack_decision.make_decision()

            if action == "attack":
                enemy["is_attacking"] = True
                enemy_animation_counters[i] += 0.2
                attack_sprites = enemy1AttackRight if enemy_directions[i] == 'right' else attackExperiment1Left
                
                if enemy_animation_counters[i] >= len(attack_sprites):
                    enemy_animation_counters[i] = 0
                    enemy["is_attacking"] = False
                
                current_frame = int(enemy_animation_counters[i])
                if current_frame >= len(attack_sprites):
                    current_frame = len(attack_sprites) - 1
                    
                enemy["sprite"] = pygame.transform.scale(
                    attack_sprites[current_frame],
                    (int(attack_sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(attack_sprites[current_frame].get_height() * ENEMY_SCALE))
                )

            elif isinstance(action, KinematicArrive):
                enemy["is_attacking"] = False
                # Aplicar comportamiento de persecución
                steering = action.get_steering()
                if steering:
                    new_x = enemy["x"] + steering.velocity.x
                    enemy["x"] = new_x
                    enemy_directions[i] = 'right' if steering.velocity.x > 0 else 'left'
                    
            elif action == "patrol":
                enemy["is_attacking"] = False
                # Comportamiento de patrulla
                if enemy_directions[i] == 'right':
                    new_x = enemy["x"] + ENEMY_SPEED
                else:
                    new_x = enemy["x"] - ENEMY_SPEED
                
                if check_collision(zoomed_world, new_x, enemy["y"]):
                    enemy_directions[i] = 'left' if enemy_directions[i] == 'right' else 'right'
                else:
                    enemy["x"] = new_x
        else:  # Experimento 2
            if enemy_directions[i] == 'right':
                new_x = enemy["x"] + ENEMY_SPEED
            else:
                new_x = enemy["x"] - ENEMY_SPEED
            
            if check_collision(zoomed_world, new_x, enemy["y"]):
                enemy_directions[i] = 'left' if enemy_directions[i] == 'right' else 'right'
            else:
                enemy["x"] = new_x
                
        # Actualizar animación
        if not enemy["is_attacking"]:
            enemy_animation_counters[i] += 0.2
            if enemy_directions[i] == 'right':
                sprites = enemy["sprites_right"]
            else:
                sprites = enemy["sprites_left"]
            
            if enemy_animation_counters[i] >= len(sprites):
                enemy_animation_counters[i] = 0
            
            current_frame = int(enemy_animation_counters[i])
            enemy["sprite"] = pygame.transform.scale(
                sprites[current_frame],
                (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                int(sprites[current_frame].get_height() * ENEMY_SCALE))
            )
        
    # Dibujar enemigos
    for enemy in enemy_positions:
        SCREEN.blit(enemy["sprite"], 
                     (enemy["x"] - camera_x - enemy["sprite"].get_width()//2,
                      enemy["y"] - camera_y - enemy["sprite"].get_height()//2))
    
    # Dibujar bombas
    for bomb in bomb_positions:
        SCREEN.blit(scaled_obstacle_bomb,
                     (bomb["x"] - camera_x - scaled_obstacle_bomb.get_width()//2,
                      bomb["y"] - camera_y - scaled_obstacle_bomb.get_height()//2))
    
    # En la sección de dibujo del bucle principal, después de dibujar el maze:
    if current_path:
        draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    
    pygame.display.flip()
    # Llamada a la función de actualización de la ventana
