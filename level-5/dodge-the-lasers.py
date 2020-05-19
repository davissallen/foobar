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

t = sqrt(2)
v(t) = v0t + at
x(t) = x0 + v0t + (a*t^2)/2
"""
import timeit


def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def get_actual_distance(time, acceleration):
    sum_nums_up_to_n = time * (time + 1) / 2
    return sum_nums_up_to_n * acceleration


def get_erringly_reported_distance(time, actual_distance):
    """i mapped out the actual vs reported distance and found that the difference =~ time / 2"""
    if time % 2 == 0:
        # even
        return long(round(actual_distance)) - long((time // 2))
    else:
        # odd
        return long(actual_distance) - long((time // 2))


def solution(time_units):
    time_units = long(time_units)
    # 1. convert actual distance using longs or custom multiplication
    actual_distance = get_actual_distance(time_units, 2**0.5)
    # 2. subtract expected difference distance from actual distance
    reported_distance = get_erringly_reported_distance(time_units, actual_distance)
    # 3. return the erringly reported distance
    return str(reported_distance)


def test_get_actual_distance():
    cases = [
        (1, 1.414213562),
        (2, 4.242640687),
        (14, 148.492424),
        (26, 496.3889604),
        (246, 42965.22224),
        (881, 549451.6675),
        (10**100, 7.07106781187e+199),
    ]
    for case in cases:
        assert is_close(get_actual_distance(case[0], 2**0.5), case[1])


def test_get_erringly_reported_distance():
    cases = [
        (1, 1, 1.41421356237310),
        (2, 3, 4.24264068711929),
        (3, 7, 8.48528137423857),
        (4, 12, 14.14213562373100),
        (5, 19, 21.21320343559640),
        (6, 27, 29.69848480983500),
        (7, 36, 39.59797974644670),
        (8, 47, 50.91168824543140),
        (9, 59, 63.63961030678930),
        (10, 73, 77.78174593052020),
        (11, 88, 93.33809511662430),
        (12, 104, 110.30865786510100),
    ]
    for case in cases:
        assert is_close(get_erringly_reported_distance(case[0], case[2]), case[1])


def test():
    f = open('cases.txt', 'r')
    lines = f.readlines()
    fails = 0
    for case in lines:
        input, output = case.split()
        answer = None
        try:
            answer = solution(input)
            assert answer == output
        except AssertionError:
            fails += 1
            print 'case {} failed. got: {}, expected: {}'.format(input, answer, output)
    print '{:.1f}% failure rate'.format(100.0 * fails / len(lines))
    print '{:.1f}% success rate'.format(100.0 * (len(lines) - fails) / len(lines))
    print '{} cases failed'.format(fails)


if __name__ == '__main__':
    time = timeit.timeit(stmt='test()', setup='from __main__ import test', number=1)
    print 'total time: {:.2f}ms'.format(time * 1000)
