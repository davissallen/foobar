"""
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and broken the bunnies out of Lambda's prison - and now you need to escape
from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations
throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in
other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods.

Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the
corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time.

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can
fit through at a time in each direction of every corridor in between,
==> figure out how many bunnies can safely make it to the escape pods at a time at peak. <==

Write a function solution(entrances, exits, path) that takes an array of integers denoting where the groups of gathered
bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of
the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances
and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going
from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most
2000000 bunnies that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step. (Note that in this example,
room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains the
same.)
"""
import timeit


def solution_old(entrances, exits, path):
    max_capacity = 2 * 10 ** 6  # 2 million, the max capacity for a room.
    # start with max bunnies in entrance rooms and 0 elsewhere.
    bunny_count = [0] * len(path)
    for entrance_room in entrances:
        bunny_count[entrance_room] = float('inf')
    visited_rooms = set(exits)
    non_exit_rooms = list(entrances)
    while non_exit_rooms:
        from_room = non_exit_rooms[0]
        non_exit_rooms.remove(from_room)
        if from_room not in visited_rooms and bunny_count[from_room]:
            visited_rooms.add(from_room)  # mark that I've been here before, so don't return.
            for to_room, corridor_capacity in enumerate(path[from_room]):
                if from_room != to_room and corridor_capacity:
                    # bunnies can travel!
                    # move bunnies to new room.
                    bunnies_able_to_travel = min(corridor_capacity, bunny_count[from_room], max_capacity)
                    bunny_count[to_room] += bunnies_able_to_travel
                    bunny_count[from_room] -= bunnies_able_to_travel
                    non_exit_rooms.append(to_room)  # go to the next room i just added bunnies to.

    bunnies_saved = 0
    for exit_room in exits:
        bunnies_saved += bunny_count[exit_room]
    return bunnies_saved


####################################################################################
# new, improved solution below to handle loops and path prioritization

max_capacity = 2 * 10 ** 6  # 2 million


def helper(corridors, exits, bunnies_in_room, current_room):
    if current_room not in bunnies_in_room:
        bunnies_in_room[current_room] = 0
        feeder_rooms = list(set([row for row in range(len(corridors)) if corridors[row][current_room] > 0]) - exits)
        feeder_rooms.sort(key=lambda x: corridors[x][current_room], reverse=True)
        for feeder_room in feeder_rooms:
            corridor_size = corridors[feeder_room][current_room]
            bunnies_to_give = min(helper(corridors, exits, bunnies_in_room, feeder_room), corridor_size, max_capacity)
            bunnies_in_room[feeder_room] -= bunnies_to_give
            bunnies_in_room[current_room] += bunnies_to_give
    return bunnies_in_room[current_room]


def solution(entrances, exits, path):
    bunnies_in_room = {room: float('inf') for room in entrances}
    bunny_count = 0
    exits = set(exits)
    for exit_room in exits:
        bunny_count += helper(path, exits, bunnies_in_room, exit_room)
    return bunny_count


def test():
    assert solution(
        [0],
        [3],
        [[0, 7, 0, 0],
         [0, 0, 6, 0],
         [0, 0, 0, 8],
         [9, 0, 0, 0]]
    ) == 6
    assert solution(
        [0, 1],
        [4, 5],
        [[0, 0, 4, 6, 0, 0],
         [0, 0, 5, 2, 0, 0],
         [0, 0, 0, 0, 4, 4],
         [0, 0, 0, 0, 6, 6],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    ) == 16
    assert solution(
        [0],
        [1],
        [[0, 7],
         [9, 0]]
    ) == 7
    assert solution(
        [0],
        [1],
        [[0, 2 * 10 ** 7],
         [9, 0]]
    ) == 2 * 10 ** 6
    assert solution(
        [2],
        [5],
        [[0, 0, 4, 6, 0, 0],
         [0, 0, 5, 2, 0, 0],
         [0, 0, 0, 0, 4, 4],
         [0, 0, 0, 0, 6, 6],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    ) == 4
    assert solution(
        [3],
        [0],
        [[0, 0, 4, 6, 0, 0],
         [0, 0, 5, 2, 0, 0],
         [0, 0, 0, 0, 4, 4],
         [0, 0, 0, 0, 6, 6],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    ) == 0
    assert solution(
        [3],
        [0],
        [[0, 0, 4, 6, 0, 0],
         [0, 0, 5, 2, 5, 0],
         [0, 0, 0, 0, 4, 4],
         [0, 0, 0, 0, 6, 6],
         [3, 0, 0, 0, 0, 0],
         [0, 10, 0, 0, 0, 0]]
    ) == 3
    assert solution(
        [0, 5],
        [2],
        [[0, 9, 4, 6, 0, 0],  # entrance
         [0, 0, 100, 2, 5, 0],
         [0, 0, 0, 0, 4, 4],  # exit
         [0, 0, 0, 0, 6, 6],
         [3, 0, 15, 0, 0, 0],
         [0, 7, 3, 0, 20, 0]]  # entrance
    ) == 38
    assert solution(
        [0],
        [3],
        [[0, 2 * 10 ** 6, 2 * 10 ** 6, 0],  # entrance
         [0, 0, 0, 2 * 10 ** 6],
         [0, 0, 0, 2 * 10 ** 6],
         [0, 0, 0, 0]]  # exit
    ) == (2 * 10 ** 6) * 2
    assert solution(
        [0],
        [5],
        [[1, 1, 0, 1, 1, 0],
         [0, 0, 0, 0, 0, 4],
         [0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    ) == 3
    assert solution(
        [0],
        [5],
        [[0, 1, 0, 1, 1, 0],
         [1, 0, 0, 0, 0, 4],
         [0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    ) == 3
    assert solution(
        [0],
        [5],
        [[0, 5, 0, 0, 0, 0],
         [0, 0, 3, 5, 0, 0],
         [0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 5],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]
    ) == 5


if __name__ == '__main__':
    ms = timeit.timeit(stmt='test()', setup='from __main__ import test', number=1000) * 1000
    print '{:.2f} ms'.format(ms)
