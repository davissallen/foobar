"""
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw
ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be
multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of
a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it
undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time
the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You
have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the
ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has
gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each
terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in
simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a
path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore
starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the
fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
"""
import timeit

import numpy

import fractions


def solution1(m):
    total_runs = 10 ** 6

    # identify terminal states
    terminal_states = set(range(len(m)))
    for state in range(len(m)):
        for possibility in m[state]:
            if possibility != 0:
                terminal_states.remove(state)
                break

    # create probabilities.
    probabilities = []
    for state in m:
        denominator = float(sum(state))
        if denominator:
            probability = []
            for likelihood in state:
                probability.append(float(fractions.Fraction(int(likelihood), int(denominator))))
            probabilities.append(probability)
        else:
            probabilities.append([0] * len(state))

    finished_states = [0] * len(m)
    states = range(len(m))
    for i in range(total_runs):
        current_state = 0
        while current_state not in terminal_states:
            probability = probabilities[current_state]
            current_state = numpy.random.choice(a=states, p=probability)
        finished_states[current_state] += 1

    for i in xrange(len(finished_states)):
        finished_states[i] = finished_states[i] / float(total_runs)

    print finished_states


def solution(t):
    """
    Implements an algorithm for solving Absolving Markov chains.
    tutorial: https://brilliant.org/wiki/absorbing-markov-chains/
    """

    if len(t) == 1:
        return [1, 1]

    # Move any terminal states to the end of the matrix.
    first_transient_state, first_terminal_state = 1, 0
    while first_terminal_state < len(t) and first_transient_state < len(t):
        if all(i == 0 for i in t[first_transient_state]):
            first_transient_state += 1
        elif any(i != 0 for i in t[first_terminal_state]):
            first_terminal_state += 1
        elif first_terminal_state < first_transient_state:
            # update references.
            for row in xrange(len(t)):
                temp = t[row][first_transient_state]
                for col in xrange(first_transient_state, first_terminal_state, -1):
                    t[row][col] = t[row][col - 1]
                t[row][first_terminal_state] = temp
            # swap lists
            t.insert(first_terminal_state, t.pop(first_transient_state))
            # increment indices.
            first_terminal_state += 1
            first_transient_state += 1
        else:
            break

    # Next, convert the probabilities matrix into fractions.
    for state in t:
        denominator = float(sum(state))
        if denominator:
            for i in xrange(len(state)):
                state[i] = state[i] / denominator

    # Find the first terminal state (assuming that terminal states are the also the final states).
    first_terminal_state = 0
    while any(i != 0 for i in t[first_terminal_state]):
        first_terminal_state += 1

    # Perform absolving markov chain algorithm.
    # transient state == state that will jump to another, it cannot end here.
    # terminal state  == state that will end, it has nothing to jump to.
    # q == transient to transient matrix
    q = [t[state][:first_terminal_state] for state in range(first_terminal_state)]
    # r == transient to terminal matrix
    r = [t[state][first_terminal_state:] for state in range(first_terminal_state)]
    # i == terminal to terminal matrix
    i = [[0] * i + [1] + [0] * (len(q) - i - 1) for i in range(len(q))]
    # I don't really understand what n means, but it's inverse of the difference between i and q
    # It must have something to do with the transition from transient to terminal states rather than transient to
    # transient or terminal to terminal.
    n = numpy.subtract(i, q)
    n = numpy.linalg.inv(n)
    # Due to my lack of understanding of n, I also don't fully understand what m is.
    # I think m must be the convergence of the transition matrices to see the probabilities of getting from any
    # transient state to any terminal state.
    m = numpy.asmatrix(n) * numpy.asmatrix(r)
    # Since we only care about the probabilities from the first state, only look at the first row of m.
    probabilities_from_initial_state = [fractions.Fraction(float(i)).limit_denominator() for i in m[0].flat]
    # Find the LCM of the denominators so we can choose one common denominator.
    lcm = int(numpy.lcm.reduce([i.denominator for i in probabilities_from_initial_state]))
    answer = [int(float(i.numerator) / float(i.denominator) * lcm) for i in probabilities_from_initial_state] + [lcm]

    return answer


def test():
    assert solution([
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]) == [3, 1, 4]
    assert solution([
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]) == [7, 6, 8, 21]
    assert solution([
        [0, 1, 0, 0, 0, 1],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [0, 3, 2, 9, 14]
    assert solution([
        [0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [4, 0, 0, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]) == [0, 3, 2, 9, 14]
    assert solution([
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 3, 2, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
    ]) == [0, 3, 2, 10, 15]  # todo: verify
    assert solution([
        [0, 1],
        [0, 0],
    ]) == [1, 1]
    assert solution([
        [0, 1, 1],
        [0, 0, 0],
        [0, 0, 0],
    ]) == [1, 1, 2]
    assert solution([
        [0, 1, 1],
        [0, 0, 0],
        [0, 0, 0],
    ]) == [1, 1, 2]
    assert solution([
        [0],
    ]) == [1, 1]
    assert solution([
        [0, 0],
        [1, 0],
    ]) == [1, 1]
    assert solution([
        [0] + [1] * 9,
        [0] * 10,
        [0] * 10,
        [0] * 10,
        [0] * 10,
        [0] * 10,
        [0] * 10,
        [0] * 10,
        [0] * 10,
        [0] * 10,
    ]) == [1] * 9 + [9]


if __name__ == '__main__':
    print timeit.timeit(stmt='test()', setup="from __main__ import test", number=1000)
    # 1.84984493256
