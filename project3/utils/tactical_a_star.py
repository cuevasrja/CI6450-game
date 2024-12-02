from typing import List 
from dataclasses import dataclass
from utils.graph import Graph
from utils.node import Node
from utils.connection import Connection
from abc import ABC, abstractmethod

class Heuristic(ABC):
    """
    ### Description
    Abstract class for a heuristic function to estimate the cost between two nodes.

    ### Attributes
    #### goal_node: Node
    The goal node to estimate the cost to.

    ### Methods
    #### estimate(from_node: Node) -> float
    Estimate the cost from the given node to the goal node.

    #### estimate_between(from_node: Node, to_node: Node) -> float
    Calculate the estimated cost between any two nodes.
    """
    def __init__(self, goal_node: Node):
        self.goal_node = goal_node
    
    def estimate(self, from_node: Node) -> float:
        return self.estimate_between(from_node, self.goal_node)
    
    @abstractmethod
    def estimate_between(self, from_node: Node, to_node: Node) -> float:
        """Calculate the estimated cost between any two nodes"""
        pass

@dataclass
class NodeRecord:
    """
    ### Description
    Record class to store information about a node during pathfinding.

    ### Attributes
    #### node: Node
    The node being recorded.

    #### connection: Connection|None
    The connection used to reach this node.

    #### cost_so_far: float
    The cost to reach this node from the start node.

    #### estimated_total_cost: float
    The estimated total cost to reach the goal node.

    ### Methods
    #### __init__(node: Node, connection: Connection|None = None, cost_so_far: float = float('inf'), estimated_total_cost: float = float('inf'))
    Initialize the record with the given values.
    """
    node: Node
    connection: Connection|None = None
    cost_so_far: float = float('inf')
    estimated_total_cost: float = float('inf')

    def __init__(self, node: Node, connection: Connection|None = None, cost_so_far: float = float('inf'), estimated_total_cost: float = float('inf')):
        self.node = node
        self.connection = connection
        self.cost_so_far = cost_so_far
        self.estimated_total_cost = estimated_total_cost

class TacticalPathfindingList:
    """
    ### Description
    Class to store a list of node records for pathfinding.

    ### Attributes
    #### records: List[NodeRecord]
    The list of node records.

    ### Methods
    #### __init__()
    Initialize the list with an empty list.

    #### __len__() -> int
    Return the number of records in the list.

    #### add(record: NodeRecord)
    Add a node record to the list.

    #### remove(record: NodeRecord)
    Remove a node record from the list.

    #### contains(node: Node) -> bool
    Check if the list contains a record for the given node.

    #### find(node: Node) -> NodeRecord|None
    Find the record for the given node in the list.

    #### smallest_element() -> NodeRecord
    Find the record with the smallest estimated total cost.
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
        return min(self.records, key=lambda x: x.estimated_total_cost)

DISTANCE_FROM_PLAYER = 200

def pathfind_tactical_astar(graph: Graph, start: Node, goal: Node, heuristic: Heuristic, player: Node) -> List[Connection]|None:
    """
    ### Description
    Perform the A* pathfinding algorithm to find the path between two nodes.

    ### Parameters
    - graph: Graph. The graph containing the nodes and connections.
    - start: Node. The starting node for the path.
    - goal: Node. The goal node to reach.
    - heuristic: Heuristic. The heuristic function to estimate the cost between nodes.
    - player: Node. The node representing the player that the path should avoid mantaing a distance of DISTANCE_FROM_PLAYER.

    ### Returns
    List[Connection]|None: The list of connections forming the path from start to goal.
    """
    # Initialize the record for the start node
    start_record = NodeRecord(
        node=start,
        cost_so_far=0,
        estimated_total_cost=heuristic.estimate(start)
    )
    
    # Initialize the open and closed lists
    open_list = TacticalPathfindingList()
    open_list.add(start_record)
    closed_list = TacticalPathfindingList()
    
    # Iterate through processing each node
    while len(open_list) > 0:
        current = open_list.smallest_element()
        
        # If it is the goal node, then terminate
        if current.node == goal:
            break
            
        # Get its outgoing connections
        connections = graph.get_connections(current.node)
        
        # Loop through each connection
        for connection in connections:
            end_node = connection.to_node
            end_node_cost = current.cost_so_far + connection.get_cost() + DISTANCE_FROM_PLAYER / (heuristic.estimate_between(end_node, player) + 1)
            
            # Handle closed list
            if closed_list.contains(end_node):
                end_node_record = closed_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
                closed_list.remove(end_node_record)
                end_node_heuristic = end_node_record.estimated_total_cost - end_node_record.cost_so_far
                
            # Handle open list
            elif open_list.contains(end_node):
                end_node_record = open_list.find(end_node)
                if end_node_record.cost_so_far <= end_node_cost:
                    continue
                end_node_heuristic = end_node_record.estimated_total_cost - end_node_record.cost_so_far
                
            # Handle unvisited nodes
            else:
                end_node_record = NodeRecord(node=end_node)
                end_node_heuristic = heuristic.estimate(end_node) + DISTANCE_FROM_PLAYER / (heuristic.estimate_between(end_node, player) + 1)
            
            # Update the node record
            end_node_record.cost_so_far = end_node_cost
            end_node_record.connection = connection
            end_node_record.estimated_total_cost = end_node_cost + end_node_heuristic
            
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
    path = []
    
    # Work back along the path
    while current.node != start:
        path.append(current.connection)
        current = closed_list.find(current.connection.from_node)
        
    # Reverse the path and return it
    path.reverse()
    return path