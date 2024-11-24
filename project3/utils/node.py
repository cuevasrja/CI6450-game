class Node:
    def __init__(self, name):
        self.name = name

class TileNode(Node):
    """
    ### Description
    A class to represent a tile node.

    ### Attributes
    - `x`: int
        The x-coordinate of the tile.
    - `y`: int
        The y-coordinate of the tile.

    ### Methods
    - `__init__(x: int, y: int) -> None`
        Initializes the TileNode object
    """
    def __init__(self, x: int, y: int):
        super().__init__(f"tile_{x}_{y}")
        self.x = x
        self.y = y