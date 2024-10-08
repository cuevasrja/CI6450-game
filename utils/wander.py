import math
import random
from pygame import Vector2
from utils.face import Face
from utils.physics import Kinematic, SteeringOutput

def random_binomial() -> float:
    """
    ### Description:
    Returns a random float between -1 and 1.

    ### Returns:
    - float : A random float between -1 and 1.
    """
    return random.uniform(-1, 1)

class Wander(Face):
    """
    ### Description
    A class to represent a wander behavior. Extends the Face class.

    ### Superclass
    Face

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Kinematic : The target to follow.
    - `maxAngularAcceleration` : float : The maximum angular acceleration of the character.
    - `maxRotation` : float : The maximum rotation of the character.
    - `targetRadius` : float : The radius to consider the target as reached.
    - `slowRadius` : float : The radius to start slowing down.
    - `wanderOffset` : float : The offset to wander.
    - `wanderRadius` : float : The radius to wander.
    - `wanderRate` : float : The rate to wander.
    - `wanderOrientation` : float : The orientation to wander.
    - `maxAcceleration` : float : The maximum acceleration of the character.

    """
    def __init__(self, character: Kinematic, target: Kinematic, maxAngularAcceleration: float, maxRotation: float, targetRadius: float, slowRadius: float, wanderOffset: float, wanderRadius: float, wanderRate: float, wanderOrientation: float, maxAcceleration: float):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius)
        self.wanderOffset: float = wanderOffset
        self.wanderRadius: float = wanderRadius
        self.wanderRate: float = wanderRate
        self.wanderOrientation: float = wanderOrientation
        self.maxAcceleration: float = maxAcceleration

    def get_steering(self) -> SteeringOutput:
        # Update the wander orientation
        self.wanderOrientation += random_binomial() * self.wanderRate

        # Calculate the combined target orientation
        targetOrientation: float = self.wanderOrientation + self.character.orientation

        # Calculate the target to delegate the face behavior
        target: Vector2 = Vector2(self.character.position.x + self.wanderOffset * math.cos(self.character.orientation), self.character.position.y + self.wanderOffset * math.sin(self.character.orientation))
        
        # Calculate the target to delegate the face behavior
        target.x += self.wanderRadius * math.cos(targetOrientation)
        target.y += self.wanderRadius * math.sin(targetOrientation)

        self.target = self.target.copy()
        self.target.position = target

        # Call the face behavior
        result: SteeringOutput = super().get_steering()

        # Set the linear acceleration to the maximum acceleration
        result.linear = Vector2(self.maxAcceleration * math.cos(self.character.orientation), self.maxAcceleration * math.sin(self.character.orientation))

        return result