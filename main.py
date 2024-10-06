# Example file showing a circle moving on screen
import random
from typing import List
import pygame
from utils.follow_path import FollowPath
from utils.look_were_are_you_going import LookWhereYoureGoing
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

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player: Kinematic = Kinematic(position=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
n_NPCs: int = 1
NPCs: List[Kinematic] = []

print("\033[1;93mBienvenido al simulador de algoritmos de movimiento\033[0m")
print("\033[1;92mSeleccione una opción: \033[0m")
print("1. Kinematic Arrive")
print("2. Kinematic Flee")
print("3. Kinematic Wandering")
print("4. Dynamic Seek")
print("5. Dynamic Flee")
print("6. Dynamic Arrive")
print("7. Align")
print("8. Velocity Match")
print("9. Face")
print("10. Look Where You're Going")
print("11. Dynamic Wander")
print("12. Path Following")

option = int(input("\033[1;92mSeleccione una opción: \033[0m"))

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
    NPCs = list_of_random_npcs(screen, 1)
    search: List[Align] = [Align(NPC, player, random.randint(10, const_velocity), 3, 1, 0.1) for NPC in NPCs]
elif option == 8:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[VelocityMatch] = [VelocityMatch(NPC, player, const_velocity) for NPC in NPCs]
elif option == 9: # Add 5 NPCs
    NPCs = list_of_random_npcs(screen, 5)
    search: List[Face] = [Face(NPC, player, random.randint(0, 50), 3, 1, 0.1) for NPC in NPCs]
elif option == 10:
    NPCs = list_of_random_npcs(screen, 1)
    search: List[LookWhereYoureGoing] = [LookWhereYoureGoing(NPC, player, random.randint(10, const_velocity), 3, 1, 0.1) for NPC in NPCs]
elif option == 11: # Add 5 NPCs
    NPCs = list_of_random_npcs(screen, 5)
    search: List[Wander] = [Wander(NPC, player, 6, random.randint(0,3), 15, 50, 50, 50, 0.5, 0.5, 300) for NPC in NPCs]
elif option == 12:
    NPCs = list_of_random_npcs(screen, 1)
    path: List[pygame.Vector2] = [pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())) for _ in range(32)]
    search: List[FollowPath] = [FollowPath(NPC, player, random.randint(10, const_velocity), path, 0.5, 0) for NPC in NPCs]
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.add_position(x=const_velocity * dt)
        hist_pos.x += const_velocity * dt
        player.set_velocity(x=const_velocity)

    if keys[pygame.K_w]:
        player.add_position(y=-const_velocity * dt)
        hist_pos.y -= const_velocity * dt
        player.set_velocity(y=-const_velocity)

    if keys[pygame.K_a]:
        player.add_position(x=-const_velocity * dt)
        hist_pos.x -= const_velocity * dt
        player.set_velocity(x=-const_velocity)
        
    if keys[pygame.K_s]:
        player.add_position(y=const_velocity * dt)
        hist_pos.y += const_velocity * dt
        player.set_velocity(y=const_velocity)

    player.set_orientation(atan2(hist_pos[0], hist_pos[1]))

    if hist_pos.x >= 10000 or hist_pos.y >= 10000:
        hist_pos = normalize(hist_pos.x, hist_pos.y)

    if player.position.y > screen.get_height():
        player.position.y = 0
    elif player.position.y < 0:
        player.position.y = screen.get_height()
        
    if player.position.x > screen.get_width():
        player.position.x = 0
    elif player.position.x < 0:
        player.position.x = screen.get_width()

    for NPC in NPCs:
        if NPC.position.y > screen.get_height() - 20:
            NPC.position.y = screen.get_height() - 20
        elif NPC.position.y < 20:
            NPC.position.y = 20

        if NPC.position.x > screen.get_width() - 20:
            NPC.position.x = screen.get_width() - 20
        elif NPC.position.x < 20:
            NPC.position.x = 20

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()