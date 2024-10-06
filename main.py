# Example file showing a circle moving on screen
from typing import List
import pygame
from utils.follow_path import FollowPath
from utils.look_were_are_you_going import LookWhereYoureGoing
from utils.wander import Wander
from utils.align import Align
from utils.arrive import Arrive
from utils.face import Face
from utils.flee import Flee
from utils.kinematic_algs import KinematicFlee, KinematicSteeringOutput, KinematicWander
from utils.drawer import draw_polygon_by_class
from utils.physics import Kinematic
from utils.seek import Seek
from utils.trigonometry import atan2, normalize
from utils.velocity_match import VelocityMatch

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.time.Clock = pygame.time.Clock()
running: bool = True
dt: int = 0
hist_pos: List[float] = [0, 0]
const_velocity: float = 300

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player: Kinematic = Kinematic(position=pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
npc: Kinematic = Kinematic(position=pygame.Vector2(10,10))

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
    search: Arrive = Arrive(npc, player, 100, 300, 10, 100)
elif option == 2:
    search: KinematicFlee = KinematicFlee(npc, player, const_velocity)
elif option == 3:
    search: KinematicWander = KinematicWander(npc, const_velocity, 6)
elif option == 4:
    search: Seek = Seek(npc, player, const_velocity)
elif option == 5:
    search: Flee = Flee(npc, player, const_velocity)
elif option == 6:
    search: Arrive = Arrive(npc, player, 100, 300, 10, 100)
elif option == 7:
    search: Align = Align(npc, player, const_velocity, 100, 100, 0.1)
elif option == 8:
    search: VelocityMatch = VelocityMatch(npc, player, const_velocity)
elif option == 9: # Add 5 NPCs
    search: Face = Face(npc, player, const_velocity, 100, 100, 0.1)
elif option == 10:
    search: LookWhereYoureGoing = LookWhereYoureGoing(npc, player, 100, 3.14, 15, 100)
elif option == 11: # Add 5 NPCs
    search: Wander = Wander(npc, player, 6, 3.14, 15, 100, 100, 100, 0.5, 0.5, 300)
elif option == 12:
    search: FollowPath = FollowPath(npc, player, const_velocity, 100, 100, 100, 100, 100)
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
    screen.fill("purple")

    steering: KinematicSteeringOutput = search.get_steering()

    if 1 <= option <= 3:
        npc.set_velocity(steering.velocity.x, steering.velocity.y)
        npc.update_with_max_speed(steering, dt, const_velocity)
    else:
        npc.set_velocity(steering.linear.x, steering.linear.y)
        npc.set_angular_velocity(steering.angular)
        npc.update(steering, dt)

    draw_polygon_by_class(screen, "red", player)
    draw_polygon_by_class(screen, "white", npc)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player.add_position(x=const_velocity * dt)
        hist_pos[0] += const_velocity *dt

    if keys[pygame.K_w]:
        player.add_position(y=-const_velocity * dt)
        hist_pos[1] -= const_velocity * dt

    if keys[pygame.K_a]:
        player.add_position(x=-const_velocity * dt)
        hist_pos[0] -= const_velocity * dt
        
    if keys[pygame.K_s]:
        player.add_position(y=const_velocity * dt)
        hist_pos[1] += const_velocity * dt

    player.set_orientation(atan2(hist_pos[0], hist_pos[1]))

    if hist_pos[0] >= 10000 or hist_pos[1] >= 10000:
        hist_pos = normalize(hist_pos[0], hist_pos[1])

    if player.position.y > screen.get_height():
        player.position.y = 0
    elif player.position.y < 0:
        player.position.y = screen.get_height()
        
    if player.position.x > screen.get_width():
        player.position.x = 0
    elif player.position.x < 0:
        player.position.x = screen.get_width()

    if npc.position.y > screen.get_height():
        npc.position.y = 0
    elif npc.position.y < 0:
        npc.position.y = screen.get_height()

    if npc.position.x > screen.get_width():
        npc.position.x = 0
    elif npc.position.x < 0:
        npc.position.x = screen.get_width()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()