import pygame, sys
from utils.game import check_collision, draw_path, find_nearest_enemy, test_player_in_range_and_zone
from utils.game_graph import GameGraph
from utils.kinematic_arrive import KinematicArrive
from utils.kinematic_arrive_descision import KinematicArriveAction, PatrolAction, InRangeDecision, AttackAction, PlayerReachedDecision
from pygame.locals import *

pygame.init()

window_width, window_height = 700, 600
SCREEN = pygame.display.set_mode((window_width,window_height))

pygame.display.set_caption("Space Invaders")

background_image = pygame.image.load("./imgs/background.jpg").convert()

ZOOM = 1.50

zoomed_world = pygame.transform.scale(
    background_image, 
    (int(background_image.get_width() * ZOOM), 
     int(background_image.get_height() * ZOOM))
)

SCREEN.blit(background_image, (0,0))

block_size = 40
game_graph = GameGraph(zoomed_world, block_size)

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
    
enemy = pygame.image.load("./imgs/enemy.png")

enemyMoveRight = [pygame.image.load(f"./imgs/enemy_r.png")]
enemyMoveLeft = [pygame.image.load(f"./imgs/enemy_l.png")]

enemyAttackRight = [pygame.image.load(f"./imgs/enemy_r.png")]
attackExperiment1Left = [pygame.image.load(f"./imgs/enemy_l.png")]

ENEMY_SPEED = 5
enemy_directions = ['right', 'right', 'left']
enemy_animation_counters = [0, 0, 0]

# Obstáculos
obs = pygame.image.load("./imgs/obstacle.png")

# Black hole sprite
black_hole = [pygame.image.load(f"./imgs/obstacle.png")]

PLAYER_SCALE = 1.5
scaled_player = pygame.transform.scale(
    standing_player,
    (int(standing_player.get_width() * PLAYER_SCALE),
     int(standing_player.get_height() * PLAYER_SCALE))
)

ENEMY_SCALE = 1.2
BOMB_SCALE = 1.5

scaled_enemy_experiment = pygame.transform.scale(
    enemy,
    (int(enemy.get_width() * ENEMY_SCALE),
     int(enemy.get_height() * ENEMY_SCALE))
)

scaled_black_hole = pygame.transform.scale(
    obs,
    (int(obs.get_width() * BOMB_SCALE),
     int(obs.get_height() * BOMB_SCALE))
)

enemy_positions = [
    {"x": 1000, "y": 650, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
    {"x": 1300, "y": 200, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
    {"x": 500, "y": 500, "sprite": scaled_enemy_experiment, "sprites_right": enemyMoveRight, "sprites_left": enemyMoveLeft, "is_attacking": False},
]

black_holes = [
    {"x": 850, "y": 1000},
    {"x": 1700, "y": 400},
    {"x": 250, "y": 150},
    {"x": 700, "y": 500}
]

space_mask = pygame.mask.from_surface(zoomed_world)

player_x = 0
player_y = 700 

WORLD_WIDTH = zoomed_world.get_width()
WORLD_HEIGHT = zoomed_world.get_height()

reloj = pygame.time.Clock()

CAMERA_MARGIN = 200
MOVE_SPEED = 5

ARRIVAL_RADIUS = 30
MAX_SPEED = 5

current_path = None
target_exp = None
current_sprite = standing_player

while True:
    # FPS
    reloj.tick(60)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    old_x = player_x
    old_y = player_y
    
    keys = pygame.key.get_pressed()
    new_x = player_x
    new_y = player_y

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
        current_path, target_exp = find_nearest_enemy(game_graph, block_size, player_x, player_y, enemy_positions)
    
        if current_path:
            next_node = current_path[0].to_node
            target_x = next_node.x * block_size
            target_y = next_node.y * block_size
            
            dx = target_x - player_x
            dy = target_y - player_y
            dist = ((dx**2 + dy**2)**0.5)
            
            if dist > 0:
                dx = dx/dist * MOVE_SPEED  
                dy = dy/dist * MOVE_SPEED
                
                new_x = player_x + dx
                new_y = player_y + dy
                
                if not check_collision(zoomed_world, new_x, new_y):
                    player_x = new_x
                    player_y = new_y
            
            draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    else:
        steps = 0
        current_sprite = standing_player if direction == 'right' else player_standing_left

    scaled_current_sprite = pygame.transform.scale(
        current_sprite,
        (int(current_sprite.get_width() * PLAYER_SCALE),
         int(current_sprite.get_height() * PLAYER_SCALE))
    )

    if not check_collision(zoomed_world, new_x, new_y):
        player_x = new_x
        player_y = new_y
    
    player_x = max(scaled_player.get_width()//2, min(WORLD_WIDTH - scaled_player.get_width()//2, player_x))
    player_y = max(scaled_player.get_height()//2, min(WORLD_HEIGHT - scaled_player.get_height()//2, player_y))
    
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
    
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(zoomed_world, (-camera_x, -camera_y))
    
    game_graph.draw_world_representation(SCREEN, camera_x, camera_y)
    
    SCREEN.blit(scaled_current_sprite, (player_x - camera_x - scaled_current_sprite.get_width()//2, 
                                         player_y - camera_y - scaled_current_sprite.get_height()//2))
    for i, enemy in enumerate(enemy_positions):
        kinematic_action = KinematicArriveAction(enemy, (player_x, player_y), MAX_SPEED, ARRIVAL_RADIUS)
        patrol_action = PatrolAction(enemy, enemy_directions[i])
            
        chase_decision = InRangeDecision(
            (enemy["x"], enemy["y"]),
            (player_x, player_y),
            kinematic_action,
            patrol_action,
            test_player_in_range_and_zone
        )
            
        attack_action = AttackAction(enemy, enemy_directions[i], enemyAttackRight, attackExperiment1Left)
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
            attack_sprites = enemyAttackRight if enemy_directions[i] == 'right' else attackExperiment1Left
            
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
            steering = action.get_steering()
            if steering:
                new_x = enemy["x"] + steering.velocity.x
                enemy["x"] = new_x
                enemy_directions[i] = 'right' if steering.velocity.x > 0 else 'left'
                
        elif action == "patrol":
            enemy["is_attacking"] = False
            if enemy_directions[i] == 'right':
                new_x = enemy["x"] + ENEMY_SPEED
            else:
                new_x = enemy["x"] - ENEMY_SPEED
            
            if check_collision(zoomed_world, new_x, enemy["y"]):
                enemy_directions[i] = 'left' if enemy_directions[i] == 'right' else 'right'
            else:
                enemy["x"] = new_x
                
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
        
    for enemy in enemy_positions:
        SCREEN.blit(enemy["sprite"], 
                     (enemy["x"] - camera_x - enemy["sprite"].get_width()//2,
                      enemy["y"] - camera_y - enemy["sprite"].get_height()//2))
    
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
    
    if current_path:
        draw_path(SCREEN, current_path, camera_x, camera_y, block_size)
    
    pygame.display.flip()
