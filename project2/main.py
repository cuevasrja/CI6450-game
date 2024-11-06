import math
import pygame, sys
from utils.game import check_collision, draw_path, find_nearest_enemy, test_player_in_range_and_zone
from utils.game_graph import GameGraph
from utils.kinematic_arrive import KinematicArrive
from utils.kinematic_arrive_descision import KinematicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision
from utils.kinematic_flee import KinematicFlee
from utils.kinematic_flee_descision import KinematicFleeAction

# Initialize Pygame
pygame.init()

# Set up the display
window_width, window_height = 700, 600
SCREEN = pygame.display.set_mode((window_width,window_height))

# Set up the window name
pygame.display.set_caption("Space Invaders")

# Load the background image
background_image = pygame.image.load("./imgs/background.jpg").convert()

# Zoom the background image
ZOOM = 1.50
zoomed_world = pygame.transform.scale(
    background_image, 
    (int(background_image.get_width() * ZOOM), 
     int(background_image.get_height() * ZOOM))
)

# Draw the background image
SCREEN.blit(background_image, (0,0))

# Create the game graph
block_size = 40
game_graph = GameGraph(zoomed_world, block_size)

# Player
camera_x = 0
camera_y = 0

standing_player = pygame.image.load("./imgs/player_r.png")
player_standing_left = pygame.image.load("./imgs/player_l.png")

player_movement_right = [pygame.image.load(f"./imgs/player_r.png")]
player_movement_left = [pygame.image.load(f"./imgs/player_l.png")]
player_movement_up = [pygame.image.load(f"./imgs/player_t.png")]
player_movement_down = [pygame.image.load(f"./imgs/player_b.png")]

steps = 0
direction = 'right'

# Enemy
# Load the enemy sprite    
enemy_stand_by = pygame.image.load("./imgs/enemy_r.png")

enemyMoveRight = [pygame.image.load(f"./imgs/enemy_r.png")]
enemyMoveLeft = [pygame.image.load(f"./imgs/enemy_l.png")]

enemyAttackRight = [pygame.image.load(f"./imgs/enemy_attack_r.png")]
enemyAttackLeft = [pygame.image.load(f"./imgs/enemy_attack_l.png")]

ENEMY_SPEED = 5
enemy_directions = ['right', 'right']
enemy_animation_counters = [0, 0]

#Variables to control the enemy
ENEMY_DETECTION_RADIUS = 100
ENEMY_FLEE_SPEED = 5
ENEMY_FLEE_MIN = 500
ENEMY_FLEE_MAX = 1700

# Obstacle
obs = pygame.image.load("./imgs/obstacle.png")

# Black hole sprite
black_hole = [pygame.image.load(f"./imgs/obstacle.png")]

# Scale the player sprite
PLAYER_SCALE = 1.5
scaled_player = pygame.transform.scale(
    standing_player,
    (int(standing_player.get_width() * PLAYER_SCALE),
     int(standing_player.get_height() * PLAYER_SCALE))
)

# Scale the enemy sprite
ENEMY_SCALE = 1.2
BOMB_SCALE = 1.5

scaled_enemy_experiment = pygame.transform.scale(
    enemy_stand_by,
    (int(enemy_stand_by.get_width() * ENEMY_SCALE),
     int(enemy_stand_by.get_height() * ENEMY_SCALE))
)


# Scale the black hole sprite
scaled_black_hole = pygame.transform.scale(
    obs,
    (int(obs.get_width() * BOMB_SCALE),
     int(obs.get_height() * BOMB_SCALE))
)

# Enemy positions
enemy_positions = [
    {"x": 1000, "y": 650, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
    {"x": 1300, "y": 200, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
]

# Black holes
black_holes = [
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
space_mask = pygame.mask.from_surface(zoomed_world)

player_x = 0
player_y = 700 

# Constants
WORLD_WIDTH = zoomed_world.get_width()
WORLD_HEIGHT = zoomed_world.get_height()

# Clock
reloj = pygame.time.Clock()

# Camera
CAMERA_MARGIN = 200

# Arrive behavior
MOVE_SPEED = 5
ARRIVAL_RADIUS = 30
MAX_SPEED = 5

# Path Finding
current_path = None
target_exp = None
current_sprite = standing_player

# Game loop
while True:
    # FPS
    reloj.tick(60)
    
    # Event loop to close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Player movement
    old_x = player_x
    old_y = player_y
    
    # Check for key presses
    keys = pygame.key.get_pressed()
    new_x = player_x
    new_y = player_y

    # Animation speed
    animation_speed = 0.5
    
    # Player movement
    if keys[pygame.K_a]: # Left
        new_x -= MOVE_SPEED
        direction = 'left'
        steps += animation_speed
        if steps >= len(player_movement_left):
            steps = 0
        current_sprite = player_movement_left[int(steps)]
    elif keys[pygame.K_d]: # Right
        new_x += MOVE_SPEED
        direction = 'right'
        steps += animation_speed
        if steps >= len(player_movement_right):
            steps = 0
        current_sprite = player_movement_right[int(steps)]
    elif keys[pygame.K_w]: # Up
        new_y -= MOVE_SPEED
        steps += animation_speed
        if steps >= len(player_movement_up):
            steps = 0
        current_sprite = player_movement_up[int(steps)]
    elif keys[pygame.K_s]: # Down
        new_y += MOVE_SPEED
        steps += animation_speed
        if steps >= len(player_movement_down):
            steps = 0
        current_sprite = player_movement_down[int(steps)]
    elif keys[pygame.K_q]: # Path Finding
        current_path, target_exp = find_nearest_enemy(game_graph, block_size, player_x, player_y, enemy_positions)
        
        # Draw the path
        if current_path:
            # Get the first node
            next_node = current_path[0].to_node
            target_x = next_node.x * block_size
            target_y = next_node.y * block_size
            
            # Calculate the direction
            dx = target_x - player_x
            dy = target_y - player_y
            dist = ((dx**2 + dy**2)**0.5)
            
            # Normalize the direction
            if dist > 0:
                dx = dx/dist * MOVE_SPEED  
                dy = dy/dist * MOVE_SPEED
                
                new_x = player_x + dx
                new_y = player_y + dy
                
                if not check_collision(zoomed_world, new_x, new_y):
                    player_x = new_x
                    player_y = new_y
            # Dr
            draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    else: # Standing
        steps = 0
        current_sprite = standing_player if direction == 'right' else player_standing_left

    # Scale the player sprite
    scaled_current_sprite = pygame.transform.scale(
        current_sprite,
        (int(current_sprite.get_width() * PLAYER_SCALE),
         int(current_sprite.get_height() * PLAYER_SCALE))
    )

    # Check for collisions
    if not check_collision(zoomed_world, new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    # Player screen position
    player_x = max(scaled_player.get_width()//2, min(WORLD_WIDTH - scaled_player.get_width()//2, player_x))
    player_y = max(scaled_player.get_height()//2, min(WORLD_HEIGHT - scaled_player.get_height()//2, player_y))
    
    # Player screen position
    player_screen_x = player_x - camera_x
    player_screen_y = player_y - camera_y
    
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
    game_graph.draw_world_representation(SCREEN, camera_x, camera_y)
    
    # Draw the player
    SCREEN.blit(scaled_current_sprite, (player_x - camera_x - scaled_current_sprite.get_width()//2, 
                                         player_y - camera_y - scaled_current_sprite.get_height()//2))
    
    # Draw the enemies
    for i, enemy in enumerate(enemy_positions):
        if i%2 == 0: # Even enemies
            # Persecution behavior
            kinematic_action = KinematicArriveAction(enemy, (player_x, player_y), MAX_SPEED, ARRIVAL_RADIUS)
            # Patrol behavior
            patrol_action = PatrolAction(enemy, enemy_directions[i])
            
            # In range decision
            chase_decision = InRangeDecision(
                (enemy["x"], enemy["y"]),
                (player_x, player_y),
                kinematic_action,
                patrol_action,
                test_player_in_range_and_zone
            )
            
            # Attack behavior
            attack_action = AttackAction(enemy, enemy_directions[i], enemyAttackRight, enemyAttackLeft)
            # Player reached decision
            attack_decision = PlayerReachedDecision(
                (enemy["x"], enemy["y"]),
                (player_x, player_y),
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
            elif isinstance(action, KinematicArrive):
                enemy["is_attacking"] = False
                # Persecution behavior
                steering = action.get_steering()
                if steering:
                    new_x = enemy["x"] + steering.velocity.x
                    new_y = enemy["y"] + steering.velocity.y
                    enemy["x"] = new_x
                    enemy["y"] = new_y
                    enemy_directions[i] = 'right' if steering.velocity.x > 0 else 'left'
            
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
        # Odd enemies
        else:
            # Flee behavior
            kinematic_flee = KinematicFleeAction(
                enemy,
                (player_x, player_y),
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
                (player_x, player_y),
                kinematic_flee,
                patrol_action,
                lambda pos1, pos2: (
                    math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2) <= ENEMY_DETECTION_RADIUS
                    and ENEMY_FLEE_MIN <= pos1[0] <= ENEMY_FLEE_MAX
                )
            )

            # Make decision
            action = flee_decision.make_decision()

            # If the player is in range, flee
            if isinstance(action, KinematicFlee):
                # Flee behavior
                steering = action.get_steering()

                # If the player is in range, flee
                if steering:
                    new_x = enemy["x"] + steering.velocity.x

                    # Limit the horizontal movement
                    if ENEMY_FLEE_MIN <= new_x <= ENEMY_FLEE_MAX:
                        enemy["x"] = new_x
                    enemy_directions[i] = 'right' if steering.velocity.x > 0 else 'left'
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
    for hole in black_holes:
        # Calculate if the player is around the black hole
        player_block_x = player_x // block_size
        player_block_y = player_y // block_size

        hole_block_x = hole["x"] // block_size
        hole_block_y = hole["y"] // block_size

        # If the player is in the same block as the black hole, the hole desappears
        if player_block_x == hole_block_x and player_block_y == hole_block_y:
            black_holes.remove(hole)
            continue
            
        if hole is not None:
            SCREEN.blit(scaled_black_hole,
                     (hole["x"] - camera_x - scaled_black_hole.get_width()//2,
                      hole["y"] - camera_y - scaled_black_hole.get_height()//2)
            )
    
    # Draw the path
    if current_path:
        draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    
    pygame.display.flip()
