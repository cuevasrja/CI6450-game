import math
from typing import Tuple

def atan2(x: float, y: float) -> float:
    """
    ### Description
    Get the angle in radians from the x-axis to the point (x, y).

    ### Parameters
    - x: float - The x-coordinate of the point.
    - y: float - The y-coordinate of the point.

    ### Returns
    - float - The angle in radians from the x-axis to the point (x, y).
    """
    if x == 0:
        if y > 0:
            return math.pi / 2
        elif y < 0:
            return -math.pi / 2
        else:
            return 0
    else:
        angle = math.atan(y / x)
        return angle if x > 0 else angle + math.pi

def new_orientation(orientation: float, velocity: Tuple[int, int]) -> float:
    """
    ### Description
    Get the new orientation of an object based on its velocity.

    ### Parameters
    - orientation: float - The current orientation of the object.
    - velocity: Tuple[int, int] - The velocity of the object.

    ### Returns
    - float - The new orientation of the object.
    """
    if velocity[0] == 0 and velocity[1] == 0:
        return orientation
    else:
        return atan2(velocity[1], velocity[0])

def in_radius(vector: Tuple[int, int], radius: float) -> bool:
    """
    ### Description
    Check if a vector is within a given radius.

    ### Parameters
    - vector: Tuple[int, int] - The vector to check.
    - radius: float - The radius to check against.

    ### Returns
    - bool - True if the vector is within the radius, False otherwise.
    """
    return vector[0] ** 2 + vector[1] ** 2 < radius ** 2

def magnitude(vector: Tuple[int, int]) -> float:
    """
    ### Description
    Get the magnitude of a vector.

    ### Parameters
    - vector: Tuple[int, int] - The vector to get the magnitude of.

    ### Returns
    - float - The magnitude of the vector.
    """
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def normalize(vector: Tuple[int, int]) -> Tuple[int, int]:
    """
    ### Description
    Normalize a vector.

    ### Parameters
    - vector: Tuple[int, int] - The vector to normalize.

    ### Returns
    - Tuple[int, int] - The normalized vector.
    """
    mag = magnitude(vector)
    return (vector[0] / mag, vector[1] / mag) if mag != 0 else (0, 0)

def rotate_vector(vector: Tuple[int, int], angle: float) -> Tuple[int, int]:
    """
    ### Description
    Rotate a vector by a given angle.

    ### Parameters
    - vector: Tuple[int, int] - The vector to rotate.
    - angle: float - The angle to rotate the vector by.

    ### Returns
    - Tuple[int, int] - The rotated vector.
    """
    x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
    y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
    return (x, y)

def map_to_range(angle: float) -> float:
	return (angle + math.pi) % (2 * math.pi) - math.pi