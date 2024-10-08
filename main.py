# Example file showing a circle moving on screen
import math
import random
from typing import List
import pygame
from utils.follow_path import FollowPath
from utils.look_were_are_you_going import LookWhereYoureGoing
from utils.game import check_border, create_square_path, key_checker, show_menu
from utils.wander import Wander
from utils.align import Align
from utils.arrive import Arrive
from utils.face import Face
from utils.flee import Flee
from utils.kinematic_algs import KinematicArrive, KinematicFlee, KinematicSteeringOutput, KinematicWander
from utils.drawer import draw_polygon_by_class
from utils.physics import Kinematic, list_of_center_npcs, list_of_random_npcs
from utils.seek import Seek
from utils.trigonometry import atan2, normalize
from utils.velocity_match import VelocityMatch

option = show_menu()

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1800, 800))
clock: pygame.time.Clock = pygame.time.Clock()
background: str = "black"
player_color: str = "blue"
npc_color: str = "red"
running: bool = True
dt: int = 0
hist_pos: pygame.Vector2 = pygame.Vector2(0, 0)
const_velocity: float = 300
const_angular_velocity: float = math.pi/2

player: Kinematic = Kinematic(position=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), angular_velocity=const_angular_velocity)
n_NPCs: int = 1
NPCs: List[Kinematic] = []

search = None

if option == 1:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[KinematicArrive] = [KinematicArrive(NPC, player, const_velocity, 100) for NPC in NPCs]
elif option == 2:
    NPCs = list_of_center_npcs(screen, 3)
    search: List[KinematicFlee] = [KinematicFlee(NPC, player, random.randint(50, const_velocity)) for NPC in NPCs]
elif option == 3:
    NPCs = list_of_center_npcs(screen, 3)
    search: List[KinematicWander] = [KinematicWander(NPC, const_velocity, random.randint(0,3)) for NPC in NPCs]
elif option == 4:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[Seek] = [Seek(NPC, player, const_velocity) for NPC in NPCs]
elif option == 5:
    NPCs = list_of_center_npcs(screen, 3)
    search: List[Flee] = [Flee(NPC, player, 50) for NPC in NPCs]
elif option == 6:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[Arrive] = [Arrive(NPC, player, 100, random.randint(50, const_velocity), 10, 100) for NPC in NPCs]
elif option == 7:
    NPCs = list_of_random_npcs(screen, 3)
    search: List[Align] = [Align(NPC, player, random.randint(10, const_velocity), 3, 1, 0.1) for NPC in NPCs]
elif option == 8:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[VelocityMatch] = [VelocityMatch(NPC, player, 10000) for NPC in NPCs]
elif option == 9: # Add 5 NPCs
    NPCs = list_of_random_npcs(screen, 5)
    search: List[Face] = [Face(NPC, player, 50, 2*math.pi, 1, 0.1) for NPC in NPCs]
elif option == 10:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[LookWhereYoureGoing] = [LookWhereYoureGoing(NPC, player, 5, 3, 1, 0.1) for NPC in NPCs]
elif option == 11: # Add 5 NPCs
    NPCs = list_of_random_npcs(screen, 5)
    search: List[Wander] = [Wander(NPC, player, 6, random.randint(0,3), 15, 50, 50, 50, 0.5, 0.5, 300) for NPC in NPCs]
elif option == 12:
    NPCs = list_of_random_npcs(screen, 1)
    path: List[pygame.Vector2] = create_square_path(screen, 36)
    search: List[FollowPath] = [FollowPath(NPC, player, const_velocity, path, 0.5, 0) for NPC in NPCs]
else:
    print("Opción inválida")
    exit()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background)

    if option == 12:
        pygame.draw.lines(screen, (80, 90, 150), True, path, 10)

    for i in range(len(NPCs)):
        steering: KinematicSteeringOutput = search[i].get_steering()

        if 1 <= option <= 3:
            NPCs[i].set_velocity(steering.velocity.x, steering.velocity.y)
            NPCs[i].update_with_max_speed(steering, dt, const_velocity)
        else:
            NPCs[i].set_velocity(steering.linear.x, steering.linear.y)
            NPCs[i].set_angular_velocity(steering.angular)
            NPCs[i].update(steering, dt)

    draw_polygon_by_class(screen, player_color, player)
    for NPC in NPCs:
        draw_polygon_by_class(screen, npc_color, NPC)

    keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
    key_checker(keys, player, hist_pos, const_velocity, dt)

    player.set_orientation(atan2(hist_pos[0], hist_pos[1]))

    hist_pos = normalize(hist_pos)

    check_border(screen, player)

    for NPC in NPCs:
        check_border(screen, NPC, 20)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()