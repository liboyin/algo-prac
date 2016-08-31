from collections import deque

class Node:
    def __init__(self, val, parent=None):
        self.val = val
        self.parent = parent  # Node
        self.children = []  # list[Node]. set during construction
        self.depth = None  # Optional[int]
        self.layer = None  # Optional[int]
        self.ancestor = None  # Optional[Node]. layer ancestor

def preprocess(root, layer_depth):  # layer_depth = sqrt(n). O(n) time
    q = deque([(root, 0, root)])  # deque[Node, int, Node]. BFS queue
    while q:
        node, depth, ancestor = q.popleft()
        node.depth = depth
        node.layer = depth // layer_depth
        if depth % layer_depth == 0:
            ancestor = node
        node.ancestor = ancestor
        for x in node.children:
            q.append((x, depth + 1, ancestor))

def LCA(a, b):  # O(\srqt n) time
    while a.layer != b.layer:
        if a.layer > b.layer:
            a = a.ancestor
        else:
            b = b.ancestor
    while a != b:
        if a.depth > b.depth:
            a = a.parent
        else:
            b = b.parent

# TODO: not tested