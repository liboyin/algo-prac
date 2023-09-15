from typing import Tuple

from comparable import T
from trees.construction import Node


def find_max_sub_bst_size(root: Node[T]) -> int:
    """
    Search the binary tree rooted at `root` to find the maximum size of a binary search tree (BST) within it.
    
    Args:
        root (Node): The root of the binary tree.
        
    Returns:
        int: The maximum size of a BST found within the binary tree.
    """
    max_size = 1

    def search_subtree(x: Node) -> Tuple[T, T, int] | None:
        """
        Helper function to recursively search for BSTs within the binary tree rooted at `x`.
        
        Args:
            x (Node): The current node being processed.
            
        Returns:
            Tuple[T, T, int] | None: A tuple containing the minimum value, maximum value, and size of the BST rooted at `x`,
                                     or None if no BST can be formed.
        """
        nonlocal max_size
        if x.left is None:
            if x.right is None:
                return x.value, x.value, 1
            q_right = search_subtree(x.right)
            if q_right is None:
                return None
            r_min, r_max, r_size = q_right
            if x.value >= r_min:
                return None
            max_size = max(max_size, r_size + 1)
            return x.value, r_max, r_size + 1
        elif x.right is None:
            q_left = search_subtree(x.left)
            if q_left is None:
                return None
            l_min, l_max, l_size = q_left
            if l_max >= x.value:
                return None
            max_size = max(max_size, l_size + 1)
            return l_min, x.value, l_size + 1
        else:
            q_left = search_subtree(x.left)
            q_right = search_subtree(x.right)
            if q_left is None or q_right is None:
                return None
            l_min, l_max, l_size = q_left
            r_min, r_max, r_size = q_right
            if not l_max < x.value < r_min:
                return None
            size = l_size + r_size + 1
            max_size = max(max_size, size)
            return l_min, r_max, size

    search_subtree(root)
    return max_size


def test_search_single_node():
    root = Node(5)
    result = find_max_sub_bst_size(root)
    assert result == 1


def test_search_balanced_bst():
    root = Node(5)
    root.left = Node(3)
    root.right = Node(7)
    root.left.left = Node(2)
    root.left.right = Node(4)
    root.right.left = Node(6)
    root.right.right = Node(8)
    result = find_max_sub_bst_size(root)
    assert result == 7


def test_search_unbalanced_bst():
    root = Node(5)
    root.left = Node(3)
    root.right = Node(7)
    root.left.left = Node(2)
    root.left.right = Node(4)
    root.right.right = Node(8)
    result = find_max_sub_bst_size(root)
    assert result == 6


def test_search_no_bst():
    root = Node(5)
    root.left = Node(3)
    root.right = Node(7)
    root.left.left = Node(2)
    root.left.right = Node(6)  # Not a BST because 6 > 5
    root.right.left = Node(9)  # Not a BST because 9 > 7
    result = find_max_sub_bst_size(root)
    assert result == 3
