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
import datetime
import decimal
from memo_util import lru_cache
import time

# since solution(n) in the worst case is be 200 digits long,
# we need to use a bigger precision limit for these calculations.
# 200 should do the trick to cover the largest case.
decimal.getcontext().prec = 200

# do some pre-computing to avoid wasted processing time.
alpha = decimal.Decimal(2).sqrt()
alpha_minus_one = alpha - 1


@lru_cache(maxsize=2 ** 15)
def sum_beatty_sequence(n):
    """
    This question happens to be a known sequence known as the Beatty sequence.
    Beatty Sequence (ref): https://oeis.org/A001951

    This solution simply sums the Beatty sequence using a recusive algorithm.
    Explanation for algorithm: https://math.stackexchange.com/a/2053713
    """
    if n == 0:
        return 0
    n1 = decimal.Decimal(alpha_minus_one * n).to_integral_exact(rounding=decimal.ROUND_FLOOR)
    p1 = n * n1
    p2 = (n * (n + 1)) / 2
    p3 = (n1 * (n1 + 1)) / 2
    p4 = sum_beatty_sequence(n1)
    return p1 + p2 - p3 - p4


def solution(time_units):
    answer = sum_beatty_sequence(long(time_units))
    return str(long(answer))


def test():
    max_case = 10 ** 100
    max_case_hundredth = max_case / 100
    square_root_two = decimal.Decimal(2).sqrt()
    pct = 0
    i = max_case
    expected = long(solution(str(i)))
    actual = None
    start = time.time()
    broken_nums = []
    while i >= 0:

        # do check.
        try:
            actual = solution(str(i))
            assert str(expected) == actual
        except AssertionError:
            broken_num = (i, expected, actual)
            broken_nums.append(broken_num)
            error_msg = '''
FAIL:
  input   : {}
  expected: {}
  actual  : {}
'''.format(i, expected, actual)
            print error_msg
            return

        # calculate new expected value.
        last_root_two_value = (i * square_root_two).to_integral_exact(rounding=decimal.ROUND_FLOOR)
        expected -= long(last_root_two_value)

        # decrement values.
        i -= 1

        # track percentage done
        if i % max_case_hundredth == 0:
            pct += 1
            eta = (((time.time() - start) / pct) * (100 - pct)) / 60.0
            print '{:3}% complete. ETA: {} minutes.'.format(pct, int(round(eta)))

    f = file('results_{}_{}.txt'.format(max_case, datetime.date.today().strftime("%Y-%m-%d")), 'w')
    if broken_nums:
        f.write('broken nums:')
        for case in broken_nums:
            f.write('input: {}, expected: {}, actual: {}'.format(*case))
    else:
        f.write('all cases passed!')
    f.close()


if __name__ == '__main__':
    assert solution(str(
        10 ** 100)) == '70710678118654752440084436210484903928483593768847403658833986899536623923105351942519376716382078638821760123411090095254685423841027253480565451739737157454059823250037671948325191776995310741236436'
    test()
