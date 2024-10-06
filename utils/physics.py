import math
import random
from typing import List, Tuple
from pygame import Vector2, Surface
from utils.trigonometry import atan2, magnitude, normalize

class Static:
    def __init__(self, position: Vector2 = Vector2(0, 0), orientation: float = 0):
        self.position: Vector2 = position
        self.orientation: float = orientation

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def set_orientation(self, angle: float):
        self.orientation = angle

    def get_position(self) -> Vector2:
        return self.position
    
    def get_orientation(self) -> float:
        return self.orientation
    
    def copy(self) -> 'Static':
        return Static(self.position, self.orientation)

class SteeringOutput:
    def __init__(self, linear: Vector2 = Vector2(0, 0), angular: float = 0):
        self.linear: Vector2 = linear
        self.angular: float = angular

class KinematicSteeringOutput:
    def __init__(self, velocity: Vector2 = Vector2(0, 0), rotation: float = 0):
        self.velocity: Vector2 = velocity
        self.rotation: float = rotation

class Kinematic:
    def __init__(self, position: Vector2 = Vector2(0, 0), orientation: float = 0, velocity: Vector2 = Vector2(0, 0), angular_velocity: float = 0):
        self.position: Vector2 = position
        self.orientation: float = orientation
        self.velocity: Vector2 = velocity
        self.angular_velocity: float = angular_velocity

    def set_position(self, x: int, y: int):
        self.position.x = x
        self.position.y = y

    def set_orientation(self, angle: float):
        self.orientation = angle

    def set_velocity(self, x: int|None = None, y: int|None = None):
        if x is not None:
            self.velocity.x = x
        if y is not None:
            self.velocity.y = y

    def set_angular_velocity(self, angular_velocity: float):
        self.angular_velocity = angular_velocity

    def get_position(self) -> Vector2:
        return self.position
    
    def get_orientation(self) -> float:
        return self.orientation

    def get_velocity(self) -> Vector2:
        return self.velocity
    
    def get_angular_velocity(self) -> float:
        return self.angular_velocity

    def update(self, steering: SteeringOutput, dt: float):
        self.position += self.velocity * dt
        self.orientation += self.angular_velocity * dt

        self.velocity += steering.linear * dt
        self.angular_velocity += steering.angular * dt

    def update_with_max_speed(self, steering: KinematicSteeringOutput, dt: float, max_speed: float):
        self.position += self.velocity * dt
        self.orientation += self.angular_velocity * dt

        if magnitude(self.velocity) > max_speed:
            self.velocity = normalize(self.velocity) * max_speed

        self.angular_velocity += steering.rotation * dt

    def add_position(self, x: int = 0, y: int = 0):
        self.position.x += x
        self.position.y += y

    def copy(self) -> 'Kinematic':
        return Kinematic(self.position, self.orientation, self.velocity, self.angular_velocity)

def random_npc(screen: Surface) -> Kinematic:
    random_x: int = random.randint(0, screen.get_width())
    random_y: int = random.randint(0, screen.get_height())
    random_orientation: float = random.uniform(0, 2 * math.pi)
    return Kinematic(Vector2(random_x, random_y), random_orientation)

def list_of_random_npcs(screen: Surface, n: int) -> List[Kinematic]:
    return [random_npc(screen) for _ in range(n)]

def center_npc(screen: Surface) -> Kinematic:
    pos_x: int = screen.get_width()//2 + random.randint(-50, 50)
    pos_y: int = screen.get_height()//2 + random.randint(-50, 50)
    random_orientation: float = random.uniform(0, 2 * math.pi)
    return Kinematic(Vector2(pos_x, pos_y), random_orientation)

def list_of_center_npcs(screen: Surface, n: int) -> List[Kinematic]:
    return [center_npc(screen) for _ in range(n)]