'''
Palindrome Linked List
https://leetcode.com/explore/challenge/card/april-leetcoding-challenge-2021/593/week-1-april-1st-april-7th/3693/

Given the head of a singly linked list, return whether it is a palindrome.

Examples:

Input: head = [1,2,2,1]
Output: True

Input: head = [1,2]
Output: False

Constraints:

1. The number of nodes in the list is in the range [1, 10 ^ 5].
2. 0 <= Node.val <= 9

The solution uses in-place reversal. It only takes linear time and constant space at the cost of destroying the data structure.
'''

from typing import List


class ListNode:
    @classmethod
    def from_list(cls, xs: List[int]) -> 'ListNode':
        nodes = [cls(x) for x in xs]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        return nodes[0]

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def count_nodes(x: ListNode) -> int:
    n = 0
    while x:
        x = x.next
        n += 1
    return n


def skip_nodes(x: ListNode, n: int) -> ListNode:
    for _ in range(n):
        x = x.next
    return x


def reverse(x: ListNode) -> ListNode:
    n = x.next
    while n:
        nn = n.next
        n.next = x
        x = n
        n = nn
    return x


def _is_palindrome(head: ListNode, tail: ListNode, n: int) -> bool:
    for _ in range(n):
        if head.val != tail.val:
            return False
        head = head.next
        tail = tail.next
    return True


def is_palindrome(head: ListNode) -> bool:
    from math import ceil
    n = count_nodes(head)
    if n == 1:
        return True
    x = skip_nodes(head, int(ceil(n / 2)))
    tail = reverse(x)  # after this step, there is a loop in the linked list
    return _is_palindrome(head, tail, n // 2)


if __name__ == '__main__':
    assert is_palindrome(ListNode.from_list([1]))
    assert is_palindrome(ListNode.from_list([1, 1]))
    assert not is_palindrome(ListNode.from_list([1, 2]))
    assert is_palindrome(ListNode.from_list([1, 2, 1]))
    assert not is_palindrome(ListNode.from_list([1, 2, 2]))
    assert is_palindrome(ListNode.from_list([1, 2, 2, 1]))
    assert not is_palindrome(ListNode.from_list([1, 2, 2, 2]))
    assert is_palindrome(ListNode.from_list([1, 2, 3, 2, 1]))
