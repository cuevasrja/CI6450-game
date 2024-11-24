import math
from sqlite3 import Connection
from typing import Dict, List
import pygame, sys
from utils.steering_output import SteeringOutput
from utils.game import check_collision, draw_path, find_nearest_enemy, key_checker, test_player_in_range_and_zone
from utils.game_graph import GameGraph
from utils.arrive import Arrive
from utils.arrive_descision import ArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision
from utils.flee import Flee
from utils.flee_descision import FleeAction
from utils.drawer import draw_polygon, draw_polygon_by_class
from utils.kinematic import Kinematic
from utils.trigonometry import atan2, normalize

# Initialize Pygame
pygame.init()

# Set up the display
window_width, window_height = 700, 600
SCREEN: pygame.Surface = pygame.display.set_mode((window_width,window_height))

# Set up the window name
pygame.display.set_caption("Space Invaders")

# Load the background image
background_image: pygame.Surface = pygame.image.load("./imgs/background.jpg").convert()

# Zoom the background image
ZOOM: float = 1.50
zoomed_world: pygame.Surface = pygame.transform.scale(
    background_image, 
    (int(background_image.get_width() * ZOOM), 
     int(background_image.get_height() * ZOOM))
)

# Draw the background image
SCREEN.blit(background_image, (0,0))

# Create the game graph
block_size: int = 40
game_graph: GameGraph = GameGraph(zoomed_world, block_size)

# Player
camera_x: int = 0
camera_y: int = 0

# Enemy
# Load the enemy sprite    
enemy_stand_by: List[pygame.Surface] = pygame.image.load("./imgs/enemy_r.png")

enemyMoveRight: List[pygame.Surface] = [pygame.image.load(f"./imgs/enemy_r.png")]
enemyMoveLeft: List[pygame.Surface] = [pygame.image.load(f"./imgs/enemy_l.png")]

enemyAttackRight: List[pygame.Surface] = [pygame.image.load(f"./imgs/enemy_attack_r.png")]
enemyAttackLeft: List[pygame.Surface] = [pygame.image.load(f"./imgs/enemy_attack_l.png")]

ENEMY_SPEED: int = 5
enemy_directions: List[str] = ['right', 'right']
enemy_animation_counters: List[int] = [0, 0]

#Variables to control the enemy
ENEMY_DETECTION_RADIUS: int = 100
ENEMY_FLEE_SPEED: int = 5
ENEMY_FLEE_MIN: int = 500
ENEMY_FLEE_MAX: int = 1700

# Obstacle
obs: pygame.Surface = pygame.image.load("./imgs/obstacle.png")

# Black hole sprite
black_hole: List[pygame.Surface] = [pygame.image.load(f"./imgs/obstacle.png")]

# Scale the enemy sprite
ENEMY_SCALE: float = 1.2
BOMB_SCALE: float = 1.5

scaled_enemy_experiment: pygame.Surface = pygame.transform.scale(
    enemy_stand_by,
    (int(enemy_stand_by.get_width() * ENEMY_SCALE),
     int(enemy_stand_by.get_height() * ENEMY_SCALE))
)


# Scale the black hole sprite
scaled_black_hole: pygame.Surface = pygame.transform.scale(
    obs,
    (int(obs.get_width() * BOMB_SCALE),
     int(obs.get_height() * BOMB_SCALE))
)

# Enemy positions
enemy_positions: List[Dict[str, int|pygame.Surface]] = [
    {"x": 1000, "y": 650, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
    {"x": 1300, "y": 200, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
]

# Black holes
black_holes: List[Dict[str, int]] = [
    {"x": 850, "y": 1000},
    {"x": 1700, "y": 400},
    {"x": 250, "y": 150},
    {"x": 700, "y": 500},
    {"x": 1000, "y": 1000},
    {"x": 1500, "y": 200},
    {"x": 2000, "y": 500},
    {"x": 2500, "y": 1000}
]

# Create the mask for the zoomed world
space_mask: pygame.Mask = pygame.mask.from_surface(zoomed_world)

player: Kinematic = Kinematic(pygame.Vector2(0, 700), angular_velocity=1)
player_orientation: float = 0
player_history: pygame.Vector2 = pygame.Vector2(0, 0)

# Constants
WORLD_WIDTH: int = zoomed_world.get_width()
WORLD_HEIGHT: int = zoomed_world.get_height()

# Clock
clock: pygame.time.Clock = pygame.time.Clock()
dt: float = 0

# Camera
CAMERA_MARGIN: int = 200

# Arrive behavior
MOVE_SPEED: int = 5
ARRIVAL_RADIUS: int = 30
SLOW_RADIUS: int = 100
MAX_SPEED: int = 5
MAX_ACCELERATION: int = 1

# Path Finding
current_path: List[Connection]|None = None
target_exp = None

# Animation speed
animation_speed: float = 0.5

# Game loop
while True:
    # Event loop to close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Player movement
    old_x = player.get_x()
    old_y = player.get_y()
    
    # Check for key presses
    keys = pygame.key.get_pressed()
    
    # Player movement
    key_checker(keys, player, player_history, MOVE_SPEED, dt, zoomed_world)
    player.set_orientation(atan2(player_history))
    player_history = normalize(player_history)
    new_x = player.get_x()
    new_y = player.get_y()

    if keys[pygame.K_q]: # Path Finding
        current_path, target_exp = find_nearest_enemy(game_graph, block_size, player.get_x(), player.get_y(), enemy_positions)
        
        # Draw the path
        if current_path:
            # Get the first node
            next_node = current_path[0].to_node
            target_x = next_node.x * block_size
            target_y = next_node.y * block_size
            
            # Calculate the direction
            dx = target_x - player.get_x()
            dy = target_y - player.get_y()
            dist = ((dx**2 + dy**2)**0.5)
            
            # Normalize the direction
            if dist > 0:
                dx = dx/dist * MOVE_SPEED  
                dy = dy/dist * MOVE_SPEED
                
                new_x = player.get_x() + dx
                new_y = player.get_y() + dy
                
                if not check_collision(zoomed_world, new_x, new_y):
                    player.add_position(dx, dy)
            # Dr
            draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    else: # No path
        current_path = None
        target_exp = None


    # Check for collisions
    if not check_collision(zoomed_world, new_x, new_y):
        player.set_position(new_x, new_y)
    
    # Player screen position
    player.set_position(
        max(10, min(WORLD_WIDTH - 10, player.get_x())),
        max(10, min(WORLD_HEIGHT - 10, player.get_y()))
    )
    
    # Player screen position
    player_screen_x = player.get_x() - camera_x
    player_screen_y = player.get_y() - camera_y
    
    # Camera
    if player_screen_x > window_width - CAMERA_MARGIN:
        camera_x += player_screen_x - (window_width - CAMERA_MARGIN)
    elif player_screen_x < CAMERA_MARGIN:
        camera_x += player_screen_x - CAMERA_MARGIN
        
    # Camera
    if player_screen_y > window_height - CAMERA_MARGIN:
        camera_y += player_screen_y - (window_height - CAMERA_MARGIN)
    elif player_screen_y < CAMERA_MARGIN:
        camera_y += player_screen_y - CAMERA_MARGIN
    
    # Camera limits
    camera_x = max(0, min(camera_x, WORLD_WIDTH - window_width))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - window_height))
    
    # Draw the background
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(zoomed_world, (-camera_x, -camera_y))
    
    # Draw the game graph
    # game_graph.draw_world_representation(SCREEN, camera_x, camera_y)
    
    # Draw the player
    draw_polygon_by_class(SCREEN, "blue", player, pygame.Vector2(camera_x, camera_y))
    
    # Draw the enemies
    for i, enemy in enumerate(enemy_positions):
        if i == 0:
            # Persecution behavior
            arrive_action = ArriveAction(enemy, (player.get_x(), player.get_y()), MAX_ACCELERATION, MAX_SPEED, ARRIVAL_RADIUS, SLOW_RADIUS)
            # Patrol behavior
            patrol_action = PatrolAction(enemy, enemy_directions[i])
            
            # In range decision
            chase_decision = InRangeDecision(
                (enemy["x"], enemy["y"]),
                (player.get_x(), player.get_y()),
                arrive_action,
                patrol_action,
                test_player_in_range_and_zone
            )
            
            # Attack behavior
            attack_action = AttackAction(enemy, enemy_directions[i], enemyAttackRight, enemyAttackLeft)
            # Player reached decision
            attack_decision = PlayerReachedDecision(
                (enemy["x"], enemy["y"]),
                (player.get_x(), player.get_y()),
                attack_action,
                chase_decision,
                ARRIVAL_RADIUS
            )
            
            # Make decision
            action = attack_decision.make_decision()

            # If the player is in range, attack
            if action == "attack":
                enemy["is_attacking"] = True
                enemy_animation_counters[i] += 0.2
                attack_sprites = enemyAttackRight if enemy_directions[i] == 'right' else enemyAttackLeft
                
                # Attack animation
                if enemy_animation_counters[i] >= len(attack_sprites):
                    enemy_animation_counters[i] = 0
                    enemy["is_attacking"] = False
                
                # Draw the attack sprite
                current_frame = int(enemy_animation_counters[i])
                if current_frame >= len(attack_sprites):
                    current_frame = len(attack_sprites) - 1
                    
                # Scale the attack sprite
                enemy["sprite"] = pygame.transform.scale(
                    attack_sprites[current_frame],
                    (int(attack_sprites[current_frame].get_width() * ENEMY_SCALE),
                    int(attack_sprites[current_frame].get_height() * ENEMY_SCALE))
                )

            # If the player is not in range, chase
            elif isinstance(action, Arrive):
                enemy["is_attacking"] = False
                # Persecution behavior
                steering: SteeringOutput = action.get_steering()
                if steering:
                    new_x = enemy["x"] + steering.linear.x
                    new_y = enemy["y"] + steering.linear.y
                    enemy["x"] = new_x
                    enemy["y"] = new_y
                    enemy_directions[i] = 'right' if steering.linear.x > 0 else 'left'
            
            # If the player is not in range and the enemy is not chasing, patrol
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
        elif i == 1:
            # Flee behavior
            flee = FleeAction(
                enemy,
                (player.get_x(), player.get_y()),
                ENEMY_FLEE_SPEED,
                ENEMY_DETECTION_RADIUS,
                WORLD_WIDTH,
                WORLD_HEIGHT,
                ENEMY_FLEE_MIN,
                ENEMY_FLEE_MAX
            )

            # Patrol behavior
            patrol_action = PatrolAction(enemy, enemy_directions[i])

            # In range decision
            flee_decision = InRangeDecision(
                (enemy["x"], enemy["y"]),
                (player.get_x(), player.get_y()),
                flee,
                patrol_action,
                lambda pos1, pos2: (
                    math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2) <= ENEMY_DETECTION_RADIUS
                    and ENEMY_FLEE_MIN <= pos1[0] <= ENEMY_FLEE_MAX
                )
            )

            # Make decision
            action = flee_decision.make_decision()

            # If the player is in range, flee
            if isinstance(action, Flee):
                # Flee behavior
                steering = action.get_steering()

                # If the player is in range, flee
                if steering:
                    new_x = enemy["x"] + steering.linear.x

                    # Limit the horizontal movement
                    if ENEMY_FLEE_MIN <= new_x <= ENEMY_FLEE_MAX:
                        enemy["x"] = new_x
                    enemy_directions[i] = 'right' if steering.linear.x > 0 else 'left'
            # If the player is not in range, patrol
            else:
                # If direction is right, move right
                if enemy_directions[i] == 'right':
                    new_x = enemy["x"] + ENEMY_SPEED
                    # If the enemy is at the right limit, change direction
                    if new_x > ENEMY_FLEE_MAX:
                        enemy_directions[i] = 'left'
                # If direction is left, move left
                else:
                    new_x = enemy["x"] - ENEMY_SPEED
                    # If the enemy is at the left limit, change direction
                    if new_x < ENEMY_FLEE_MIN:
                        enemy_directions[i] = 'right'

                # Check for collisions    
                if check_collision(zoomed_world, new_x, enemy["y"]):
                    enemy_directions[i] = 'left' if enemy_directions[i] == 'right' else 'right'
                else:
                    enemy["x"] = new_x
        elif i == 2:
            pass
        
        # If the enemy is not attacking, animate the enemy
        if not enemy["is_attacking"]:
            # Animation speed
            enemy_animation_counters[i] += 0.2

            # If the enemy is moving right, use the right sprites
            if enemy_directions[i] == 'right':
                sprites = enemy["sprites_right"]
            # If the enemy is moving left, use the left sprites
            else:
                sprites = enemy["sprites_left"]
            
            # Enemy animation
            if enemy_animation_counters[i] >= len(sprites):
                enemy_animation_counters[i] = 0
            
            # Draw the enemy sprite
            current_frame = int(enemy_animation_counters[i])
            enemy["sprite"] = pygame.transform.scale(
                sprites[current_frame],
                (int(sprites[current_frame].get_width() * ENEMY_SCALE),
                int(sprites[current_frame].get_height() * ENEMY_SCALE))
            )

    
    # Draw the enemies
    for enemy in enemy_positions:
        SCREEN.blit(enemy["sprite"], 
                     (enemy["x"] - camera_x - enemy["sprite"].get_width()//2,
                      enemy["y"] - camera_y - enemy["sprite"].get_height()//2))
    
    # Draw the black holes
    for i, hole in enumerate(black_holes):
        if hole is None:
            continue
        # Calculate if the player is around the black hole
        player_block_x = player.get_x() // block_size
        player_block_y = player.get_y() // block_size

        hole_block_x = hole["x"] // block_size
        hole_block_y = hole["y"] // block_size

        # If the player is in the same block as the black hole, the hole desappears
        if player_block_x == hole_block_x and player_block_y == hole_block_y:
            black_holes[i] = None
            continue
            
        if hole is not None:
            SCREEN.blit(scaled_black_hole,
                     (hole["x"] - camera_x - scaled_black_hole.get_width()//2,
                      hole["y"] - camera_y - scaled_black_hole.get_height()//2)
            )
    
    # Draw the path
    if current_path:
        draw_path(SCREEN, current_path, camera_x, camera_y, block_size)

    # FPS
    dt =  clock.tick(60) / 30
    
    pygame.display.flip()
