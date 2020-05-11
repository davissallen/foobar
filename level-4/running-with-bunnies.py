"""
Running with Bunnies
====================

You and your rescued bunny prisoners need to get out of this collapsing death trap of a space station - and fast!
Unfortunately, some of the bunnies have been weakened by their long imprisonment and can't run very fast. Their friends
are trying to help them, but this escape would go a lot faster if you also pitched in. The defensive bulkhead doors have
begun to close, and if you don't make it through in time, you'll be trapped! You need to grab as many bunnies as you can
and get through the bulkheads before they close.

The time it takes to move from your starting point to all of the bunnies and to the bulkhead will be given to you in a
square matrix of integers. Each row will tell you the time it takes to get to the start, first bunny, second bunny, ...,
last bunny, and the bulkhead in that order. The order of the rows follows the same pattern (start, each bunny,
bulkhead). The bunnies can jump into your arms, so picking them up is instantaneous, and arriving at the bulkhead at the
same time as it seals still allows for a successful, if dramatic, escape. (Don't worry, any bunnies you don't pick up
will be able to escape with you since they no longer have to carry the ones you did pick up.) You can revisit different
spots if you wish, and moving to the bulkhead doesn't mean you have to immediately leave - you can move to and from the
bulkhead to pick up additional bunnies if time permits.

In addition to spending time traveling between bunnies, some paths interact with the space station's security
checkpoints and add time back to the clock. Adding time to the clock will delay the closing of the bulkhead doors, and
if the time goes back up to 0 or a positive number after the doors have already closed, it triggers the bulkhead to
reopen. Therefore, it might be possible to walk in a circle and keep gaining time: that is, each time a path is
traversed, the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most bunnies you can pick up and which bunnies
they are, while still escaping through the bulkhead before the doors close for good. If there are multiple sets of
bunnies of the same size, return the set of bunnies with the lowest prisoner IDs (as indexes) in sorted order. The
bunnies are represented as a sorted list by prisoner ID, with the first bunny being 0. There are at most 5 bunnies, and
time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[  #0  #1  #2  #3   #4
  [ 0,  2,  2,  2,  -1],  #0 = Start
  [ 9,  0,  2,  2,  -1],  #1 = Bunny 0
  [ 9,  3,  0,  2,  -1],  #2 = Bunny 1
  [ 9,  3,  2,  0,  -1],  #3 = Bunny 2
  [ 9,  3,  2,  2,   0],  #4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point, bunny 0, bunny 1, bunny 2, and the
bulkhead door exit respectively. You could take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best combination for this space station hallway, so
the answer is [1, 2].

-- Python cases --
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]
"""


def has_negative_cycle(graph):
    d = [float('inf') for _ in xrange(len(graph))]
    d[0] = 0
    for i in xrange(len(graph)):
        flag = False
        for u in xrange(len(graph)):
            for v in xrange(len(graph)):
                if d[u] + graph[u][v] < d[v]:
                    d[v] = d[u] + graph[u][v]
                    flag = True
        if flag:
            break
    for u in xrange(len(graph)):
        for v in xrange(len(graph)):
            if d[u] + graph[u][v] < d[v]:
                return True
    return False


def helper(times, time_remaining, from_room, rooms_visited):
    """rooms_visited, a set, will also act as the bunny counter with len()."""
    pass


def solution(times, time_limit):
    """explore all situations"""

    # look for negative cycles.
    # if there are negative cycles, return all the bunnies.
    if has_negative_cycle(times):
        return range(1, len(times) - 1)

    # base case.
    # if no negative loops and time limit is <= 0, i can get no bunnies.
    # if there are no negative cycles, continue.
    if time_limit <= 0:
        return []

    # want to know: fastest route to exit for every room.
    # this will help me make my quitting decision... i think.
    # for that I can use the bellman-ford algorithm.
    pass

    # explore all possible paths, choosing the next path greedily.
    pass


def test():
    pass


if __name__ == '__main__':

    cases = [
        ([
            [0, 2, 2, 2, -1],
            [9, 0, 2, 2, -1],
            [9, 3, 0, 2, -1],
            [9, 3, 2, 0, -1],
            [9, 3, 2, 2,  0]
        ], 1, [1, 2], False),
        ([
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ], 3, [0, 1], False),
        ([
            [0, 1, 1, 1, 1],
            [1, 0, 1, -5, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ], 2, [1, 2, 3], True),
    ]

    for case in cases:
        assert has_negative_cycle(case[0]) == case[3]
        assert solution(case[0], case[1]) == case[2]
