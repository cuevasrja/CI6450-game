from typing import Tuple
import pygame
from utils.trigonometry import atan2, magnitude, normalize

class Static:
    def __init__(self, position: Tuple[int, int] = (0, 0), orientation: float = 0):
        self.position: Tuple[int, int] = position
        self.orientation: float = orientation

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def set_orientation(self, angle: float):
        self.orientation = angle

    def get_position(self) -> Tuple[int, int]:
        return self.position
    
    def get_orientation(self) -> float:
        return self.orientation

class SteeringOutput:
    def __init__(self, linear: Tuple[int, int] = (0, 0), angular: float = 0):
        self.linear: Tuple[int, int] = linear
        self.angular: float = angular

class Kinematic:
    def __init__(self, position: Tuple[int, int] = (0, 0), orientation: float = 0, velocity: Tuple[int, int] = (0, 0), angular_velocity: float = 0):
        self.position: Tuple[int, int] = position
        self.orientation: float = orientation
        self.velocity: Tuple[int, int] = velocity
        self.angular_velocity: float = angular_velocity

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def set_orientation(self, angle: float):
        self.orientation = angle

    def set_velocity(self, x: int, y: int):
        self.velocity = (x, y)

    def set_angular_velocity(self, angular_velocity: float):
        self.angular_velocity = angular_velocity

    def get_position(self) -> Tuple[int, int]:
        return self.position
    
    def get_orientation(self) -> float:
        return self.orientation

    def get_velocity(self) -> Tuple[int, int]:
        return self.velocity
    
    def get_angular_velocity(self) -> float:
        return self.angular_velocity

    def update(self, steering: SteeringOutput, dt: float):
        self.position += self.velocity * dt
        self.orientation += self.angular_velocity * dt

        self.velocity += steering.linear * dt
        self.angular_velocity += steering.angular * dt

    def update_with_max_speed(self, steering: SteeringOutput, dt: float, max_speed: float):
        self.position += self.velocity * dt
        self.orientation += self.angular_velocity * dt

        self.velocity += steering.linear * dt
        if magnitude(self.velocity) > max_speed:
            self.velocity = normalize(self.velocity) * max_speed

        self.angular_velocity += steering.angular * dt
