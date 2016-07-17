#Algorithmic Problems with Solutions
##String
###Needle in a haystack
####Single pattern
* Knuth-Morris-Pratt algorithm: $O(n)$, shortest code
* Boyer-Moore algorithm: Worst $O(mn)$, fastest in practise
* Rabin-Karp algorithm (rolling hash): Expected $O(n)$
* Z algorithm TODO

####Multiple patterns
* Aho-Corasick algorithm: $O(n)$, FSA similar to KMP

###Palindromes
####Longest palindromic substring
* Binary search is not valid: 'aba' does not contain palindrome of length 2
* Longest common substring with reverse is not valid: consider 'abcdefcba'
* Manacher’s algorithm: $O(n)$
* Suffix tree: $O(n)$ TODO

####Palindrome of length k
* Rolling hash: Expected $O(n)$

####Longest palindromic subsequence
* Longest common subsequence with reverse: $O(n)$

####Palindrome after removing at most k characters
* Delete-only edit distance with reverse <= 2k: $O(nk)$, limit search space to +-k around diagonal

###Longest common substring
* Suffix tree: $O(n)$ TODO
* Rolling hash + binary search: $O(n\log n)$

###Longest common subsequence
* Convert to longest increasing subsequence: $O(n\log n)$

###Longest repeated substring
* Suffix tree: $O(n)$

## Sorting

###Order statistics
* QuickSelect algorithm: Expected $O(n)$, worst $O(n^2)$
* Blum, Floyd, et al. 1973: $O(n)$

###Longest increasing subsequence
* Dynamic programming: $O(n^2)$
* Binary search: $O(n\log n)$

###Longest consecutive subarray

###Longest consecutive subsequence

###Longest alternating subsequence
* Greedy search of turning points: $O(n)$

###Zero-sum subarray
* Also: Longest subarray with equal number of -1 and 1
* Hashing partial sums: $O(n)$

## TODO
长度为N的序列Sequence=abc….Z，问有多少不同的二叉树形态中序遍历是这个，写递推公式
给定整数n和m，问能不能找出整数x，使得x以后的所有整数都可以由整数n和m组合而成
中序遍历二叉树，利用O(1)空间统计遍历的每个节点的层次，写bug free的code
一个运算序列只有+、*、数字，计算运算序列的结果