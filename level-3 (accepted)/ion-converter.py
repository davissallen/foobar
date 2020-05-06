"""
Ion Flux Relabeling
===================

Oh no! Commander Lambda's latest experiment to improve the efficiency of her LAMBCHOP doomsday device has backfired
spectacularly. She had been improving the structure of the ion flux converter tree, but something went terribly wrong
and the flux chains exploded. Some of the ion flux converters survived the explosion intact, but others had their
position labels blasted off. She's having her henchmen rebuild the ion flux converter tree by hand, but you think you
can do it much more quickly - quickly enough, perhaps, to earn a promotion!

Flux chains require perfect binary trees, so Lambda's design arranged the ion flux converters to form one. To label
them, she performed a post-order traversal of the tree of converters and labeled each converter with the order of that
converter in the traversal, starting at 1. For example, a tree of 7 converters would look like the following:

   7
 3   6
1 2 4 5

Write a function solution(h, q) - where h is the height of the perfect tree of converters and q is a list of positive
integers representing different flux converters - which returns a list of integers p where each element in p is the
label of the converter that sits on top of the respective converter in q, or -1 if there is no such converter.  For
example, solution(3, [1, 4, 7]) would return the converters above the converters at indexes 1, 4, and 7 in a perfect
binary tree of height 3, which is [3, 6, -1].

The domain of the integer h is 1 <= h <= 30, where h = 1 represents a perfect binary tree containing only the root,
h = 2 represents a perfect binary tree with the root and two leaf nodes, h = 3 represents a perfect binary tree with the
root, two internal nodes and four leaf nodes (like the example above), and so forth.  The lists q and p contain at least
one but no more than 10000 distinct integers, all of which will be between 1 and 2^h-1, inclusive.
"""
import random
import time


def solution(height, flux_converters):
    """returns a list of converters that each sit above the respective flux_converters[i]

    time complexity: O(nlog(k)) where n = number of converters and k = the size of each converter
    space complexity: O(1)

    ~ I could consider keeping a store of powers of two, but I don't think it's worth it. I guess I could make that list
    of powers of two and binary search it for the number i need, but the list is only size 30, so it wouldn't make that
    much of a performance difference to offset the size... or would it?
    """
    answers = []

    # todo: consider pre-populating a powers of two list
    # powers_of_two = [2**i for i in range(31)]

    for converter in flux_converters:

        if converter >= 2 ** height - 1:
            answers.append(-1)
            continue

        # find i where 2**i-1 > num
        idx, curr = 0, 1
        while curr - 1 <= converter:
            curr *= 2
            idx += 1

        # calculate left and right subnodes
        left = right = curr = curr - 1
        while converter not in [left, right]:
            curr = left if converter < left else right
            left = curr - 2 ** (idx - 1)
            right = curr - 1
            idx -= 1

        answers.append(curr)

    return answers


if __name__ == '__main__':
    assert solution(3, [2, 3, 6, 7, 8, 25, 31]) == [3, 7, 7, -1, -1, -1, -1]
    assert solution(3, [1, 4, 7]) == [3, 6, -1]
    assert solution(3, [7, 3, 5, 1]) == [-1, 7, 6, 3]
    assert solution(5, [19, 14, 28]) == [21, 15, 29]
    assert solution(29, [19, 14, 28]) == [21, 15, 29]

    start = time.time()
    solution(30, [random.randint(1, 2 ** 31) for i in range(10000)])
    print(time.time() - start)
