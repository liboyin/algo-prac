from collections import deque

class Node:
    def __init__(self, char, next=None, term=None, fail=None):
        # default parameters are only initialised once, hence are not suitable for mutable objects
        self.char = char
        self.next = dict() if next is None else next
        self.term = [] if term is None else term
        self.fail = fail

def build_trie(keywords):
    root = Node(char=None)
    root.fail = root
    for kwd in keywords:
        cursor = root
        for c in kwd:
            if c in cursor.next:  # existing node, move forward
                cursor = cursor.next[c]
            else:  # create new node, move forward
                new_node = Node(char=c)
                cursor.next[c] = new_node
                if cursor is root:
                    new_node.fail = root  # all nodes with depth 1 fail to root
                cursor = new_node
        cursor.term = [kwd]
    queue = deque([root])
    while queue:  # bfs to find longest proper suffix, layer by layer
        cursor = queue.popleft()
        for probe in cursor.next.values():  # for each next char of cursor, set fail pointer
            queue.append(probe)
            fail_target = cursor.fail  # start with the longest proper suffix of the longest proper prefix
            # if none of cursor's fail targets' next chars is the same as cursor's next char, then fall back
            while fail_target is not root and probe.char not in fail_target.next:
                fail_target = fail_target.fail
            probe.fail = fail_target.next[probe.char] if fail_target is not cursor else root
            # equivalent to: probe.fail = root if (fail_target is root and probe.char not in root.next) else fail_target.next[probe.char]
            probe.term += probe.fail.term
    return root

def search(text, ps):
    root = build_trie(ps)
    cursor = root
    for i, c in enumerate(text):
        while cursor is not root and c not in cursor.next:
            cursor = cursor.fail
        if c in cursor.next:
            cursor = cursor.next[c]
            if cursor.term:
                yield (i, cursor.term)

if __name__ == '__main__':
    for i, ps in search('abccab', ['a', 'ab', 'bab', 'bc', 'bca', 'c', 'caa']):
        print('{}: {}'.format(i, ps))
