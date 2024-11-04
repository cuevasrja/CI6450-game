import math
from pygame import Vector2

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

def new_orientation(orientation: float, velocity: Vector2) -> float:
    """
    ### Description
    Get the new orientation of an object based on its velocity.

    ### Parameters
    - orientation: float - The current orientation of the object.
    - velocity: Vector2 - The velocity of the object.

    ### Returns
    - float - The new orientation of the object.
    """
    if velocity.x == 0 and velocity.y == 0:
        return orientation
    else:
        return atan2(velocity.y, velocity.x)

def in_radius(vector: Vector2, radius: float) -> bool:
    """
    ### Description
    Check if a vector is within a given radius.

    ### Parameters
    - vector: Vector2 - The vector to check.
    - radius: float - The radius to check against.

    ### Returns
    - bool - True if the vector is within the radius, False otherwise.
    """
    return vector.x ** 2 + vector.y ** 2 < radius ** 2

def magnitude(vector: Vector2) -> float:
    """
    ### Description
    Get the magnitude of a vector.

    ### Parameters
    - vector: Vector2 - The vector to get the magnitude of.

    ### Returns
    - float - The magnitude of the vector.
    """
    return math.sqrt(vector.x ** 2 + vector.y ** 2)

def normalize(vector: Vector2) -> Vector2:
    """
    ### Description
    Normalize a vector.

    ### Parameters
    - vector: Vector2 - The vector to normalize.

    ### Returns
    - Vector2 - The normalized vector.
    """
    mag = magnitude(vector)
    return Vector2(vector.x / mag, vector.y / mag) if mag != 0 else Vector2(0, 0)

def rotate_vector(vector: Vector2, angle: float) -> Vector2:
    """
    ### Description
    Rotate a vector by a given angle.

    ### Parameters
    - vector: Vector2 - The vector to rotate.
    - angle: float - The angle to rotate the vector by.

    ### Returns
    - Vector2 - The rotated vector.
    """
    x = vector.x * math.cos(angle) - vector.y * math.sin(angle)
    y = vector.x * math.sin(angle) + vector.y * math.cos(angle)
    return Vector2(x, y)

def map_to_range(angle: float) -> float:
	return (angle + math.pi) % (2 * math.pi) - math.pi