from collections import deque
from dataclasses import dataclass, field
from typing import Deque, List, Optional, Tuple

@dataclass
class Node:
    val: int
    parent: 'Optional[Node]' = None
    children: List['Node'] = field(default_factory=list)
    # following attributes will be set in self.preprocess()
    node_level: int = 0
    jump_level: int = 0
    ancestor_for_jump: 'Node' = field(init=False)
    
    def __post_init__(self):
        self.ancestor_for_jump = self

def preprocess(root: Node, jump_interval: int) -> None:
    """
    Preprocesses the tree rooted at `root` to calculate each node's level,
    jump level, and ancestor for jump. The preprocessing is done to speed
    up the LCA calculation later.

    Parameters:
    - root (Node): The root node of the tree.
    - jump_interval (int): The interval at which jump ancestors are set.

    Returns:
    None
    """
    q: Deque[Tuple[Node, int, Node]] = deque([(root, 0, root)])  # BFS queue
    while q:
        node, node_level, ancestor_for_jump = q.popleft()
        node.node_level = node_level
        node.jump_level = node_level // jump_interval
        if node_level % jump_interval == 0:
            ancestor_for_jump = node
        node.ancestor_for_jump = ancestor_for_jump
        for x in node.children:
            q.append((x, node_level + 1, ancestor_for_jump))


def lowest_common_ancestor(a: Node, b: Node) -> Node:
    """
    Finds the Lowest Common Ancestor (LCA) of nodes `a` and `b` in a tree.
    Assumes that the tree has been preprocessed using the `preprocess` function.

    Parameters:
    - a (Node): The first node.
    - b (Node): The second node.

    Returns:
    Node: The Lowest Common Ancestor (LCA) of `a` and `b`.
    """
    while a.jump_level != b.jump_level:
        if a.jump_level > b.jump_level:
            a = a.ancestor_for_jump
        else:
            b = b.ancestor_for_jump
    while a != b:
        if a.node_level > b.node_level:
            a = a.parent
        else:
            b = b.parent
    return a


def test_lowest_common_ancestor():
    root = Node(1)
    child1 = Node(2, root)
    child2 = Node(3, root)
    child1_1 = Node(4, child1)
    child1_2 = Node(5, child1)
    child2_1 = Node(6, child2)
    root.children = [child1, child2]
    child1.children = [child1_1, child1_2]
    child2.children = [child2_1]
    preprocess(root, 2)
    lca_node = lowest_common_ancestor(child1_1, child2_1)
    assert lca_node.val == 1
