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
import timeit
from collections import OrderedDict


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


def get_shortest_path(times, current_room, exit_room, rooms_unvisited, total_path):
    """seems to work!"""
    if current_room == exit_room:
        return total_path
    elif not rooms_unvisited:
        return float('inf')
    else:
        options = []
        for next_room in rooms_unvisited:
            new_unvisited_rooms = [room for room in rooms_unvisited if room != next_room]
            options.append(
                get_shortest_path(
                    times,
                    next_room,
                    exit_room,
                    new_unvisited_rooms,
                    total_path + times[current_room][next_room]
                )
            )
        return min(options)


def helper_rec(memory, shortest_paths_to_exit, exit, times, time_remaining, current_room, sets_of_bunnies_saved, bunnies_saved_so_far):
    if memory[current_room].get(len(bunnies_saved_so_far)) >= time_remaining:
        return
    else:
        memory[current_room][len(bunnies_saved_so_far)] = time_remaining

    if any(len(i) == len(times) - 2 for i in sets_of_bunnies_saved):
        return

    if current_room == exit:
        sets_of_bunnies_saved.add(frozenset(sorted(bunnies_saved_so_far)))

    if time_remaining >= shortest_paths_to_exit[current_room]:
        for next_room, time_cost in times[current_room].iteritems():
            if next_room != current_room:
                # make deep copy of set and add current bunny
                new_bunnies = bunnies_saved_so_far.copy()
                if 0 < current_room < len(times) - 1:
                    new_bunnies.add(current_room - 1)
                helper_rec(
                    memory,
                    shortest_paths_to_exit,
                    exit,
                    times,
                    time_remaining - time_cost,
                    next_room,
                    sets_of_bunnies_saved,
                    new_bunnies
                )


def solution(times, time_limit):
    """explore all situations"""

    # if there are negative cycles, return all the bunnies, else continue.
    if has_negative_cycle(times):
        return range(len(times) - 2)

    # want to know: fastest route to exit for every room.
    # this will help me make my quitting decision... i think.
    # for that I can use the bellman-ford algorithm.
    shortest_paths_to_exit = []
    for room in xrange(len(times)):
        shortest_paths_to_exit.append(get_shortest_path(times, room, len(times) - 1, xrange(1, len(times)), 0))

    # create a times list that is sorted by distance.
    times_by_distance = []
    for t in times:
        paths_sorted_by_distance = OrderedDict(sorted({room: distance for room, distance in enumerate(t)}.items(), key=lambda x: x[1]))
        times_by_distance.append(paths_sorted_by_distance)

    # explore all possible paths, exiting when it's hopeless.
    bunnies_saved = set()
    memory = {room: {0: -float('inf')} for room in xrange(len(times))}
    helper_rec(
        memory=memory,
        shortest_paths_to_exit=shortest_paths_to_exit,
        exit=len(times) - 1,
        times=times_by_distance,
        time_remaining=time_limit,
        current_room=0,
        sets_of_bunnies_saved=bunnies_saved,
        bunnies_saved_so_far=set()
    )
    max_len = 0
    best_bunnies = []
    bunnies_saved = [list(i) for i in bunnies_saved]
    for bunny_set in bunnies_saved:
        if len(bunny_set) > max_len:
            best_bunnies = bunny_set
        elif len(bunny_set) == max_len and sum(bunny_set) < sum(best_bunnies):
            best_bunnies = bunny_set
        max_len = max(max_len, len(bunny_set))

    return sorted(best_bunnies)


def test():
    cases = [
        ([
             [0, 1, 1],
             [9, 0, 1],
             [9, 3, 0],
         ], 1, [], False),
        ([
             [0, 1, 1],
             [9, 0, 1],
             [9, 3, 0],
         ], 2, [0], False),
        ([
             [0, 1, -1, 1],
             [9, 0, 2, 1],
             [9, 1, 0, 1],
             [9, 3, 2, 0],
         ], 2, [0, 1], False),
        ([
             [0, 2, 2, 2, -1],
             [9, 0, 2, 2, -1],
             [9, 3, 0, 2, -1],
             [9, 3, 2, 0, -1],
             [9, 3, 2, 2, 0]
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
         ], 2, [0, 1, 2], True),
        ([
             [0, 2, 2, 2, 1],
             [9, 0, 4, 4, 100],
             [9, 3, 0, 2, 1],
             [9, 3, 2, 0, 100],
             [9, 3, 2, 2, 0]
         ], 5, [1, 2], False),
        ([
             [0, 2, 2, 1, 1],
             [9, 0, 2, 2, 100],
             [9, 3, 0, 2, 1],
             [9, 3, 2, 0, 100],
             [9, 3, 2, 2, 0]
         ], 3, [1], False),
        ([
             [0, 1, 1, 1, 1],
             [1, 0, 1, 1, 1],
             [1, 1, 0, 1, 1],
             [1, 1, 1, 0, 1],
             [1, 1, 1, 1, 0]
         ], 1, [], False),
        ([
             [0, 1, 1, 1, 1],
             [1, 0, 1, 1, 1],
             [1, 1, 0, 1, 1],
             [1, 1, 1, 0, 1],
             [1, 1, 1, 1, 0]
         ], 999, [0, 1, 2], False),
    ]

    for idx, case in enumerate(cases):
        try:
            assert has_negative_cycle(case[0]) == case[3]
            assert solution(case[0], case[1]) == case[2]
        except AssertionError:
            print 'Case {} FAILED.'.format(idx)


if __name__ == '__main__':
    time = timeit.timeit(stmt='test()', setup='from __main__ import test', number=100)
    print 'total time: {:.2f}ms'.format(time * 1000)
