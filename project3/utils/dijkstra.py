from typing import List
from dataclasses import dataclass
from utils.graph import Graph
from utils.node import Node
from utils.connection import Connection

@dataclass
class NodeRecord:
    """
    ### Description
    A record for a node in the pathfinding algorithm.

    ### Attributes
    - `node`: The node.

    ### Optional Attributes
    - `connection`: The connection to the node.
    - `cost_so_far`: The cost to reach the node.

    ### Methods
    - `__init__(node: Node, connection: Connection|None = None, cost_so_far: float = float('inf'))`: Initializes
    the record with the given node, connection, and cost.
    """
    def __init__(self, node: Node, connection: Connection|None = None, cost_so_far: float = float('inf')):
        self.node = node
        self.connection = connection
        self.cost_so_far = cost_so_far

    node: Node
    connection: Connection|None = None
    cost_so_far: float = float('inf')

class PathfindingList:
    """
    ### Description
    A list of node records used in the pathfinding algorithm.

    ### Attributes
    - `records`: The list of node records.

    ### Methods
    - `__init__()`: Initializes the list with an empty list.
    - `__len__()`: Returns the number of records in the list.
    - `add(record: NodeRecord)`: Adds a record to the list.
    - `remove(record: NodeRecord)`: Removes a record from the list.
    - `contains(node: Node) -> bool`: Returns whether the list contains a node.
    - `find(node: Node) -> NodeRecord|None`: Finds a record in the list.
    - `smallest_element() -> NodeRecord`: Returns the record with the smallest cost so far.
    """
    def __init__(self):
        self.records: List[NodeRecord] = []
    
    def __len__(self):
        return len(self.records)
    
    def add(self, record: NodeRecord):
        self.records.append(record)
    
    def remove(self, record: NodeRecord):
        self.records.remove(record)
    
    def contains(self, node: Node) -> bool:
        return any(record.node == node for record in self.records)
    
    def find(self, node: Node) -> NodeRecord|None:
        for record in self.records:
            if record.node == node:
                return record
        return None
    
    def smallest_element(self) -> NodeRecord:
        return min(self.records, key=lambda x: x.cost_so_far)

def pathfind_dijkstra(graph: Graph, start: Node, goal: Node) -> List[Connection]|None:
    # Initialize the record for the start node
    start_record = NodeRecord(node=start, cost_so_far=0)
    
    # Initialize the open and closed lists
    open_list = PathfindingList()
    open_list.add(start_record)
    closed_list = PathfindingList()
    
    # Iterate through processing each node
    while len(open_list) > 0:
        current: NodeRecord = open_list.smallest_element()
        
        # If it is the goal node, then terminate
        if current.node == goal:
            break
            
        # Get its outgoing connections
        connections: List[Connection] = graph.get_connections(current.node)
        
        # Loop through each connection
        for connection in connections:
            end_node: Node = connection.to_node
            end_node_cost: float = current.cost_so_far + connection.get_cost()
            
            # Skip if the node is closed
            if closed_list.contains(end_node):
                continue
                
            # Check if node is open
            elif open_list.contains(end_node):
                end_node_record: NodeRecord|None = open_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
            else:
                end_node_record = NodeRecord(node=end_node)
                
            # Update the node record
            end_node_record.cost_so_far = end_node_cost
            end_node_record.connection = connection
            
            # Add it to open list if not already there
            if not open_list.contains(end_node):
                open_list.add(end_node_record)
                
        # Move current node from open to closed
        open_list.remove(current)
        closed_list.add(current)
    
    # Return null if no path found
    if current.node != goal:
        return None
        
    # Compile the path
    path: List[Connection] = []
    
    # Work back along the path
    while current.node != start:
        path.append(current.connection)
        current = closed_list.find(current.connection.from_node)
        
    # Reverse the path and return it
    path.reverse()
    return path