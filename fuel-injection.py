"""
Fuel Injection Perfection
=========================

Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for her
LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit of
sabotage while you're at it - so you took the job gladly.

Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each
need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to figure
out the most efficient way to sort and shift the pellets down to a single pellet at a time.

The fuel control mechanisms have three operations:

1) Add one fuel pellet
2) Remove one fuel pellet
3) Divide the entire group of fuel pellets by 2 (due to the destructive energy released when a quantum antimatter pellet
is cut in half, the safety controls will only allow this to happen if there is an even number of pellets)

Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of
operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up to
309 digits long, so there won't ever be more pellets than you can express in that many digits.

For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1

-- Python cases --
Input:
solution.solution('15')
Output:
    5

Input:
solution.solution('4')
Output:
    2
"""


def helper1(pellets, cycles):
    if pellets == 1:
        return cycles
    elif pellets % 2 == 0:
        return min(
            helper1(pellets/2, cycles+1),
            helper1(pellets-1, cycles+1),
            helper1(pellets+1, cycles+1),
        )
    else:
        return min(
            helper1(pellets-1, cycles+1),
            helper1(pellets+1, cycles+1),
        )


def helper2(pellets):
    cycles = 0

    while pellets > 1:

        higher_power_of_two = (pellets - 1).bit_length()
        lower_power_of_two = higher_power_of_two - 1

        distance_to_higher = 2**higher_power_of_two - pellets
        distance_to_lower = pellets - 2**lower_power_of_two

        closer_step = 1 if distance_to_higher < distance_to_lower else -1

        if pellets % 2 == 1:
            # odd, have to take a step.
            pellets += closer_step
        elif closer_step == 1:
            # even
            if distance_to_higher <= higher_power_of_two:
                pellets /= 2
            else:
                pellets += 1
            pass
        else:
            # even
            if distance_to_lower <= lower_power_of_two:
                pellets /= 2
            else:
                pellets -= 1

        cycles += 1

    return cycles


def plus_one(binary, end_idx):
    original_idx = end_idx
    while end_idx >= 0 and binary[end_idx] == '1':
        binary[end_idx] = '0'
        end_idx -= 1
    else:
        if end_idx == -1:
            binary.insert(0, '1')
            return original_idx + 1
        else:
            binary[end_idx] = '1'
            return original_idx


def minus_one(binary, end_idx):
    binary[end_idx] = '0'


def helper(pellets):
    binary = [i for i in bin(pellets)][2:]
    idx = len(binary) - 1
    count = 0
    while idx > 0:
        # print ''.join(binary[:idx+1])
        if binary[idx] == '0':
            idx -= 1
            # print('divide')
        elif binary[idx-1] == '0':
            minus_one(binary, idx)
            # print('subtract')
        elif binary[idx-1] == '1':
            if idx == 1:
                minus_one(binary, idx)
                # print('subtract')
            else:
                idx = plus_one(binary, idx)
                # print('add')
        count += 1
    return count


def solution(n):
    return helper(int(n))


if __name__ == '__main__':
    assert solution('1') == 0
    assert solution('2') == 1
    assert solution('3') == 2
    assert solution('4') == 2
    assert solution('5') == 3
    assert solution('6') == 3
    assert solution('15') == 5
    assert solution('27') == 7
    assert solution('22') == 6

    # for i in range(33):
    #     print '{}: {}'.format(i, solution(str(i)))

    print solution('3093092840983120943908198334890710439827987189478237456948762397846519870843172049870918253468974362578962038974574319085718945789464361716745386159564012840930928409831209831209309309284098312094390819833489071089478237456948762397846519870843172049870918253468974362578962038974574319085718945789464361716745386159564012840930928409831209831209')
