from typing import Tuple
import pygame
from trigonometry import new_orientation

class Static:
    def __init__(self, position: Tuple[int, int] = (0, 0), orientation: float = 0):
        self.position: Tuple[int, int] = position
        self.orientation: float = orientation

    @staticmethod
    def set_position(x: int, y: int):
        Static.position = (x, y)

    @staticmethod
    def set_orientation(angle: float):
        Static.orientation = angle

    @staticmethod
    def get_position() -> Tuple[int, int]:
        return Static.position
    
    @staticmethod
    def get_orientation() -> float:
        return Static.orientation

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

    @staticmethod
    def set_position(x: int, y: int):
        Kinematic.position = (x, y)

    @staticmethod
    def set_orientation(angle: float):
        Kinematic.orientation = angle

    @staticmethod
    def set_velocity(x: int, y: int):
        Kinematic.velocity = (x, y)

    @staticmethod
    def set_angular_velocity(angular_velocity: float):
        Kinematic.angular_velocity = angular_velocity

    @staticmethod
    def get_position() -> Tuple[int, int]:
        return Kinematic.position
    
    @staticmethod
    def get_orientation() -> float:
        return Kinematic.orientation

    @staticmethod
    def get_velocity() -> Tuple[int, int]:
        return Kinematic.velocity
    
    @staticmethod
    def get_angular_velocity() -> float:
        return Kinematic.angular_velocity

    @staticmethod
    def update(steering: SteeringOutput, dt: float):
        Kinematic.position += Kinematic.velocity * dt
        Kinematic.orientation += Kinematic.angular_velocity * dt

        Kinematic.velocity += steering.linear * dt
        Kinematic.angular_velocity += steering.angular * dt

class KinematicSteeringOutput:
    def __init__(self, velocity: Tuple[int, int] = (0, 0), rotation: float = 0):
        self.velocity: Tuple[int, int] = velocity
        self.rotation: float = rotation

class KinematicSeek:
    def __init__(self, character: Static, target: Static, max_speed: float):
        self.character: Static = character
        self.target: Static = target
        self.max_speed: float = max_speed

    @staticmethod
    def get_steering() -> KinematicSteeringOutput:
        steering: KinematicSteeringOutput = KinematicSteeringOutput()

        steering.velocity = KinematicSeek.target.position - KinematicSeek.character.position
        steering.velocity = steering.velocity.normalize() * KinematicSeek.max_speed

        KinematicSeek.character.orientation = new_orientation(KinematicSeek.character.orientation, steering.velocity)

        steering.rotation = 0
        return steering
