import os
import sys
from contextlib import contextmanager

@contextmanager
def suppress_stdout():
    with open(os.devnull, 'w') as devnull:
        default = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = default

class Mutable:  # a wrapper class to share an immutable object, e.g. a number
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        assert type(self.val) == type(other)
        return self.val + other

    def __iadd__(self, other):
        assert type(self.val) == type(other)
        self.val += other
        return self

    def __sub__(self, other):
        assert type(self.val) == type(other)
        return self.val - other

    def __repr__(self):
        return str(self.val)

    def __str__(self):
        return self.__repr__()

class SuffixTree:
    class Node:
        count = 0

        def __init__(self, start, end, link=None):
            """
            :param start: int. Starting index of the substring represented by the edge to self. For root, start is ineffective.
            :param end: Union[Mutable[int], int]. Ending index (inclusive) of the substring represented by the edge to self.
                As a result, the length of the substring represented by the edge to self is end - start + 1.
                For leaf nodes, end is the shared mutable global ending index; for internal nodes, end is an immutable int.
                For root, end is ineffective.
            :param link: Optional[Node]. Rule D: every internal node with char sequence (from root) s has a suffix link to
                another internal node with char sequence s1, where s1 is the immediate proper suffix of s, i.e len(s1) == len(s) - 1.
                A newly created internal node links to root. link is None iff self is the root or a leaf node.
            :var next: dict[char, Node]. Children nodes indexed by their first char. next is empty (but not None) iff self is leaf.
            :var label: int. Each instance of SuffixTree.Node is uniquely labelled by its time of instantiation.
            """
            self.start = start
            self.end = end
            self.next = dict()
            self.link = link
            self.label = SuffixTree.Node.count
            SuffixTree.Node.count += 1

        def __repr__(self):
            return 'id={}, start={}, end={}, next.keys={}, link={}'\
                .format(self.label, self.start, self.end, list(self.next.keys()), 'None' if self.link is None else self.link.label)

        def __str__(self):
            return self.__repr__()

    class Active:
        def __init__(self, node, edge, length):
            """
            Active point denotes the position of the NEXT char in the current suffix tree: from node, following the
                direction of t[edge], walk length steps. Each SuffixTree has only one instance of Active.
            :param node: SuffixTree.Node
            :param edge: int. Index of the directional char.
            :param length: int. Number of steps, starting from 0. By rule A, length == 0 -> edge is ineffective.
            """
            self.node = node
            self.edge = edge
            self.length = length

        def __repr__(self):
            return 'node=({}), edge={}, length={}'.format(self.node, self.edge, self.length)

        def __str__(self):
            return self.__repr__()

    def __init__(self, text, verbose=False):
        assert text[-1] not in text[:-1]
        self.t = text
        self.root = SuffixTree.Node(start=-1, end=-1)
        self.active = SuffixTree.Active(node=self.root, edge=-1, length=0)
        self.remain = 0  # number of remaining suffices to be inserted
        self.end = Mutable(-1)  # shared (mutable) index of the current char. when finished, end == len(text)
        if not verbose:
            with suppress_stdout():
                for i, c in enumerate(self.t):
                    self.step(i, c)
        else:
            for i, c in enumerate(self.t):
                self.step(i, c)
        assert self.remain == 0

    def step(self, i, c):
        a = self.active
        self.end += 1
        self.remain += 1
        last_link = None
        while self.remain > 0:
            print('i={}, c=\'{}\', remain={}, a=({})'.format(i, c, self.remain, a))
            if a.length == 0:  # rule A: a.node is only canonicalised when a.length > a.node.end - a.node.start + 1
                assert a.node is self.root  # by rule A, a.length == 0 -> a.node is root
                assert self.remain == 1
                # two ways to reach a.length == 0: 1. it has never grown; 2. decreased from a.length == 1. both leads to remain == 1
                if c in a.node.next:
                    a.edge = i  # correct a.edge at root guarantees correct direction during canonicalisation
                    a.length = 1
                    print('\ta.length == 0 and c in a.node.next')
                    print('\tupdated a=({})'.format(a))
                    break  # rule B: if the input char is found, then break and move to the next input char
                else:  # this must be the last iteration for c: insertion of c itself at root
                    a.node.next[c] = SuffixTree.Node(start=i, end=self.end)
                    print('\ta.length == 0 and c not in a.node.next')
                    print('\tinserted leaf node: {}[\'{}\']=({})'.format(a.node.label, c, a.node.next[c]))
                    self.remain -= 1  # equivalent to self.remain = 0
                    # rule C: after creating a leaf node (could be a by-product of an internal node), decrease remain
            else:
                c1 = self.next_char(c)  # a.node may or may not have been advanced during canonicalisation
                n = a.node.next[self.t[a.edge]]  # target node of a.edge. rule A -> effective a.edge
                if c1 is None:  # c is expected at the head of n, but it is not there
                    print('\tc1=None, n=({})'.format(n))
                    n.next[c] = SuffixTree.Node(start=i, end=self.end)
                    print('\tinserted leaf node: {}[\'{}\']=({})'.format(n.label, c, n.next[c]))
                    self.next_suffix(last_link, n)  # by rule D, suffix link is not just between newly created nodes
                    last_link = n
                    self.remain -= 1  # rule C
                elif c1 == c:
                    print('\tc1={}, n=({})'.format(c, n))
                    if last_link is not None:
                        last_link.link = n  # rule D. may be executed multiple times with identical last_link
                    print('\tlast_link={}'.format(n.label))
                    a.length += 1
                    print('\tupdated a=({})'.format(a))
                    break  # rule B
                else:  # c1 != c
                    print('\tc1={}, n=({})'.format(c1, n))
                    x = SuffixTree.Node(start=n.start, end=n.start + a.length - 1, link=self.root)
                    # rule D. note that x.end is now an immutable int
                    x.next[self.t[x.start + a.length]] = n  # x is inserted between a.node and n
                    x.next[c] = SuffixTree.Node(start=i, end=self.end)  # new leaf node as a by-product of x
                    print('\tinserted leaf node: {}[\'{}\']=({})'.format(x.label, c, x.next[c]))
                    a.node.next[self.t[n.start]] = x  # x is a child of a, replacing n
                    print('\tinserted internal node: {}[\'{}\']=({})'.format(a.node.label, self.t[n.start], x))
                    n.start += a.length
                    print('\ttransplanted leaf node: {}[\'{}\']=({})'.format(x.label, self.t[x.start + a.length], n))
                    self.next_suffix(last_link, x)
                    last_link = x
                    self.remain -= 1  # rule C

    def next_suffix(self, old, new):
        """
        Completes the suffix link, and moves the active point to the insertion point of t[i - (remain - 1)].
        :param old: SuffixTree.Node. last node in the suffix link
        :param new: SuffixTree.Node. new node in the suffix link
        :return: None
        """
        if old is not None:
            print('\t\tsuffix link: {} -> {}'.format(old.label, new.label))
            old.link = new  # old node points to new node. rule D
        a = self.active
        if a.node is self.root:  # rule E.1: if a.node is root, then move to the immediate proper suffix by increasing a.edge
            a.edge += 1
            a.length -= 1
        else:
            a.node = a.node.link  # rule E.2: otherwise, move to the immediate proper suffix by suffix jump
        print('\t\tupdated a=({})'.format(a))
        print('\t\tlast_link={}'.format(new.label))

    def next_char(self, c):
        """
        Returns the next char in the current suffix tree, as defined by the active point. If the current active point
        happens to be the head of its own child x, the current input char c is considered: if c is on the head of x, c
        is returned. Otherwise, None is returned. If the current active point is beyond the head of x, it is canonicalised
        by advancing to be as close to the active point as possible.
        :param c: current input char
        :return: Optional[char]
        """
        a = self.active
        n = a.node.next[self.t[a.edge]]  # target node of a.edge
        print('\t\tn=({})'.format(n))
        l = n.end - n.start + 1  # length of the substring represented by a.edge
        if a.length < l:  # next char is on a.edge
            print('\t\tnext char is on the edge a -> n')
            return self.t[n.start + a.length]
        if a.length == l:  # next char is on the head of n, but it may or may not be c
            print('\t\tnext char is on the head of n')
            return c if c in n.next else None
        # elif a.length > l:  # rule A
        print('\t\tnext char is beyond the head of n')
        a.node = n
        a.length -= l
        a.edge += l
        print('\t\tcanonicalised a=({})'.format(a))
        return self.next_char(c)  # recursive call

def validate(st):
    """
    Verifies whether a suffix tree encodes all suffices of the full text it encodes.
    :param st: SuffixTree
    :return: bool
    """
    def contains(r, p):
        """
        Recursively verifies whether a partial suffix tree contains a text sequence.
        :param r: SuffixTree.Node. Root of the partial suffix tree.
        :param p: str. Partial text sequence.
        :return: bool
        """
        if len(p) == 0:
            return True
        if p[0] not in r.next:
            return False
        n = r.next[p[0]]
        l = n.end - n.start + 1
        if t[n.start: n.end + 1] == p[:l]:
            return contains(n, p[l:])  # recursive call
        return False
    t = st.t
    for i in range(len(t)):
        if not contains(st.root, t[i:]):
            print('validation failed at {}'.format(t[i:]))
            return False
    return True

if __name__ == '__main__':
    from random import choice
    from strings import ascii_lowercase as alphabet
    std_test = ['adeacdade', 'abcabxabcd', 'abcdefabxybcdmnabcdex', 'abcadak', 'abcabxabcd', 'mississippi', 'banana',
                'ooooooooo', 'cddcdc', 'dedododeodo']
    for x in std_test:
        assert validate(SuffixTree(x + '$', verbose=True))
    for _ in range(100):
        x = ''.join(choice(alphabet) for _ in range(50)) + '$'
        assert validate(SuffixTree(x, verbose=True))
