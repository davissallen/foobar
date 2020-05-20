# coding=utf-8
"""
Dodge the Lasers!
=================

Oh no! You've managed to escape Commander Lambdas collapsing space station in an escape pod with the rescued bunny
prisoners - but Commander Lambda isn't about to let you get away that easily. She's sent her elite fighter pilot
squadron after you - and they've opened fire!

Fortunately, you know something important about the ships trying to shoot you down. Back when you were still Commander
Lambdas assistant, she asked you to help program the aiming mechanisms for the starfighters. They undergo rigorous
testing procedures, but you were still able to slip in a subtle bug.

The software works as a time step simulation:

if it is tracking a target that is accelerating away at 45 degrees, the software will consider the targets acceleration
to be equal to the square root of 2, adding the calculated result to the targets end velocity at each timestep.

However, thanks to your bug, instead of storing the result with proper precision, it will be truncated to an integer
before adding the new velocity to your current position. This means that instead of having your correct position, the
targeting software will erringly report your position as sum(i=1..n, floor(i*sqrt(2))) - not far enough off to fail
Commander Lambdas testing, but enough that it might just save your life.

If you can quickly calculate the target of the starfighters' laser beams to know how far off they'll be, you can trick
them into shooting an asteroid, releasing dust, and concealing the rest of your escape.

Write a function solution(str_n) which, given the string representation of an integer n, returns the sum of
(floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. That is, for every number i in the range 1
to n, it adds up all of the integer portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".

str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be very large (up to 101 digits!), using
just sqrt(2) and a loop won't work. Sometimes, it's easier to take a step back and concentrate not on what you have in
front of you, but on what you don't.

-- Python cases --
Input:
solution.solution('77')
Output:
    4208

Input:
solution.solution('5')
Output:
    19
"""
import timeit

import numpy as np


def sum_beatty_sequence(alpha, n):
    """
    Sums the Beatty sequence that takes an alpha that meets 1 < alpha < 2.
    Beatty Sequence: https://oeis.org/A001951
    Explanation for solution: https://math.stackexchange.com/a/2053713
    """
    if n == 0:
        return 0
    n1 = np.floor((alpha - 1) * n)
    p1 = n * n1
    p2 = n * (n + 1) / 2
    p3 = n1 * (n1 + 1) / 2
    p4 = sum_beatty_sequence(alpha, n1)
    return p1 + p2 - p3 - p4


def solution(time_units):
    return str(long(sum_beatty_sequence(np.sqrt(2), long(time_units))))


def test():
    f = open('generated_cases.csv', 'r')
    lines = f.readlines()
    fails = 0
    print 'starting checks'
    for input, output in enumerate(lines):
        answer = None
        try:
            answer = solution(input + 1)
            assert answer == output[:-1]
        except AssertionError:
            fails += 1
            # first case that fails:
            # case 93222358 failed. got: 6145046469361799, expected: 6145046469361800
            print 'case {} failed. got: {}, expected: {}'.format(input + 1, answer, output)
            return
    print '{} cases failed'.format(fails)


if __name__ == '__main__':
    time = timeit.timeit(stmt='test()', setup='from __main__ import test', number=1)
    print 'total time: {:.2f}ms'.format(time * 1000)
