from abc import ABC, abstractmethod

class DecisionTreeNode(ABC):
    """
    ### Description
    A node in a decision tree.

    ### Attributes
    - `true_node`: The node to traverse if the decision is true.
    - `false_node`: The node to traverse if the decision is false.

    ### Methods
    - `make_decision()`: Returns the node to traverse.
    """
    @abstractmethod
    def make_decision(self):
        pass

class Action(DecisionTreeNode):
    """
    ### Description
    A leaf node in a decision tree.

    ### Methods
    - `make_decision()`: Returns the node itself.
    """
    def make_decision(self):
        return self

class Decision(DecisionTreeNode):
    """
    ### Description
    A decision node in a decision tree.

    ### Attributes
    - `true_node`: The node to traverse if the decision is true.
    - `false_node`: The node to traverse if the decision is false.

    ### Methods
    - `test_value()`: Returns the value to test.
    - `get_branch()`: Returns the node to traverse based on the test value.
    - `make_decision()`: Returns the node to traverse.
    """
    def __init__(self, true_node: DecisionTreeNode, false_node: DecisionTreeNode):
        self.true_node = true_node
        self.false_node = false_node

    @abstractmethod
    def test_value(self):
        pass

    def get_branch(self):
        if self.test_value():
            return self.true_node
        return self.false_node

    def make_decision(self):
        branch = self.get_branch()
        return branch.make_decision()