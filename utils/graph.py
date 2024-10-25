from typing import List
from pygame import Vector2

class Node:
    def __init__(self, id: int, coords: Vector2) -> None:
        self.id: int = id
        self.coords = coords

    def __str__(self) -> str:
        return f"Node {self.id} at ({self.coords.x}, {self.coords.y})"
    
    def __repr__(self) -> str:
        return f"Node {self.id} at ({self.coords.x}, {self.coords.y})"
    
    def __eq__(self, other) -> bool:
        return self.id == other.id and self.coords == other.coords
    
    def __lt__(self, other) -> bool:
        return self.id < other.id
    
    def __le__(self, other) -> bool:
        return self.id <= other.id
    
    def __gt__(self, other) -> bool:
        return self.id > other.id
    
    def __ge__(self, other) -> bool:
        return self.id >= other.id
    
    def __ne__(self, other) -> bool:
        return self.id != other.id
    
    def __add__(self, other) -> Vector2:
        return self.coords + other.coords
    
    def __sub__(self, other) -> Vector2:
        return self.coords - other.coords
    
    def __mul__(self, other) -> Vector2:
        if isinstance(other, Node):
            return self.coords * other.coords
        elif isinstance(other, Vector2):
            return self.coords * other
        elif type(other) == int:
            return self.coords * other
        else:
            return NotImplemented
    
    def __truediv__(self, other) -> Vector2:
        if isinstance(other, Node):
            return self.coords / other.coords
        elif isinstance(other, Vector2):
            return self.coords / other
        elif type(other) == int:
            return self.coords / other
        else:
            return NotImplemented
        
    def __floordiv__(self, other) -> Vector2:
        if isinstance(other, Node):
            return self.coords // other.coords
        elif isinstance(other, Vector2):
            return self.coords // other
        elif type(other) == int:
            return self.coords // other
        else:
            return NotImplemented

    def __mod__(self, other) -> Vector2:
        if isinstance(other, Node):
            return self.coords % other.coords
        elif isinstance(other, Vector2):
            return self.coords % other
        elif type(other) == int:
            return self.coords % other
        else:
            return NotImplemented

    def __pow__(self, other) -> Vector2:
        if isinstance(other, Node):
            return self.coords ** other.coords
        elif isinstance(other, Vector2):
            return self.coords ** other
        elif type(other) == int:
            return self.coords ** other
        else:
            return NotImplemented
    
class Connection:
    def __init__(self, id: int, node1: Node, node2: Node) -> None:
        self.id: int = id
        self.node1: Node = node1
        self.node2: Node = node2
        self.cost: float = (node1.coords - node2.coords).length()

    def get_cost(self) -> float:
        return self.cost
    
    def get_from_node(self) -> Node:
        return self.node1
    
    def get_to_node(self) -> Node:
        return self.node2
    
    def __str__(self) -> str:
        return f"Connection between {self.node1.id} and {self.node2.id} with cost {self.cost}"
    
    def __repr__(self) -> str:
        return f"Connection between {self.node1.id} and {self.node2.id} with cost {self.cost}"
    
    def __eq__(self, other) -> bool:
        return self.node1 == other.node1 and self.node2 == other.node2 and self.cost == other.cost
    
    def __lt__(self, other) -> bool:
        return self.cost < other.cost
    
    def __le__(self, other) -> bool:
        return self.cost <= other.cost
    
    def __gt__(self, other) -> bool:
        return self.cost > other.cost
    
    def __ge__(self, other) -> bool:
        return self.cost >= other.cost
    
    def __ne__(self, other) -> bool:
        return self.cost != other.cost
    
class Graph:
    def __init__(self) -> None:
        self.nodes: List[Node] = []
        self.connections: List[Connection] = []
    
    def add_node(self, coords: Vector2) -> None:
        i: int = len(self.nodes)
        self.nodes.append(Node(i, coords))
    
    def add_connection(self, v: Node, w: Node) -> None:
        self.connections.append(Connection(v, w))
    
    def get_node(self, id: int) -> Node:
        return self.nodes[id]
    
    def get_connection(self, node1: Node, node2: Node) -> Connection|None:
        for connection in self.connections:
            if connection.node1 == node1 and connection.node2 == node2:
                return connection
        return None
    
    def get_connections(self, node: Node) -> List[Connection]:
        return [connection for connection in self.connections if connection.node1 == node or connection.node2 == node]

    def __str__(self) -> str:
        return f"Graph with {len(self.nodes)} nodes and {len(self.connections)} connections"
    
    def __repr__(self) -> str:
        return f"Graph with {len(self.nodes)} nodes and {len(self.connections)} connections"
    
def reconstruct_path(came_from: dict, current: Node) -> List[Node]:
    total_path: List[Node] = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path
