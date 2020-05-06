"""
Bomb, Baby!
===========

You're so close to destroying the LAMBCHOP doomsday device you can taste it! But in order to do so, you need to deploy
special self-replicating bombs designed for you by the brightest scientists on Bunny Planet. There are two types: Mach
bombs (M) and Facula bombs (F). The bombs, once released into the LAMBCHOP's inner workings, will automatically deploy
to all the strategic points you've identified and destroy them at the same time.

But there's a few catches. First, the bombs self-replicate via one of two distinct processes:
a) Every Mach bomb retrieves a sync unit from a Facula bomb; for every Mach bomb, a Facula bomb is created;
b) Every Facula bomb spontaneously creates a Mach bomb.

For example, if you had 3 Mach bombs and 2 Facula bombs, they could either produce
a) 3 Mach bombs and 5 Facula bombs, or
b) 5 Mach bombs and 2 Facula bombs.
The replication process can be changed each cycle.

Second, you need to ensure that you have exactly the right number of Mach and Facula bombs to destroy the LAMBCHOP
device. Too few, and the device might survive. Too many, and you might overload the mass capacitors and create a
singularity at the heart of the space station - not good!

And finally, you were only able to smuggle one of each type of bomb - one Mach, one Facula - aboard the ship when you
arrived, so that's all you have to start with. (Thus it may be impossible to deploy the bombs to destroy the LAMBCHOP,
but that's not going to stop you from trying!)

You need to know how many replication cycles (generations) it will take to generate the correct amount of bombs to
destroy the LAMBCHOP. Write a function solution(M, F) where M and F are the number of Mach and Facula bombs needed.
Return the fewest number of generations (as a string) that need to pass before you'll have the exact number of bombs
necessary to destroy the LAMBCHOP, or the string "impossible" if this can't be done! M and F will be string
representations of positive integers no larger than 10^50. For example, if M = "2" and F = "1", one generation would
need to pass, so the solution would be "1". However, if M = "2" and F = "4", it would not be possible.

-- Python cases --
Input:
solution.solution('4', '7')
Output:
    4

Input:
solution.solution('2', '1')
Output:
    1
"""
from datetime import datetime


def helper1(target_m, target_f, m, f, cycles_completed):
    if target_f == f and target_m == m:
        # success!
        return cycles_completed
    elif f > target_f or m > target_m:
        # FAIL.
        return float('inf')
    else:
        return min(
            helper1(target_m, target_f, m + f, f, cycles_completed + 1),
            helper1(target_m, target_f, m, m + f, cycles_completed + 1)
        )


def solution1(target_m, target_f):
    answer = helper1(int(target_m), int(target_f), 1, 1, 0)
    if answer == float('inf'):
        return 'impossible'
    else:
        return str(answer)


# todo: convert to iterative. max recursion depth is exceeded
def helper2(target_high, target_low, a, b, cycles_completed, memory):
    key = high, low = (a, b) if a > b else (b, a)
    if high > target_high or low > target_low:
        # found an answer or exceeded the bounds, quit.
        return
    elif cycles_completed >= memory.get(key, float('inf')):
        # been here before, and quicker, quit.
        return
    else:
        # never been here before this fast.
        memory[key] = cycles_completed
        helper2(target_high, target_low, high + low, low, cycles_completed + 1, memory)
        helper2(target_high, target_low, high, high + low, cycles_completed + 1, memory)


def solution2(m, f):
    memory = {}
    high, low = (int(m), int(f)) if int(m) > int(f) else (int(f), int(m))
    helper2(high, low, 1, 1, 0, memory)
    try:
        answer = memory[(int(high), int(low))]
    except KeyError:
        answer = 'impossible'
    return str(answer)


def helper3(smaller, bigger):
    memory = {(1, 1): 0}

    cycles_completed = 1
    queue = [(1, 1), ]
    temp = []
    while queue:
        bombs = queue.pop()
        a, b = bombs[0], bombs[1]

        if a > bigger or b > smaller:
            continue

        op1 = (a + b, a if a > b else b)
        op2 = (a + b, b if a > b else a)

        if op1 in memory and memory.get(op1) <= cycles_completed:
            # do nothing? quit somehow?
            pass
        else:
            # update memory and continue.
            memory[op1] = cycles_completed
            temp.append(op1)

        if op2 in memory and memory.get(op2) <= cycles_completed:
            # do nothing? quit somehow?
            pass
        else:
            # update memory and continue.
            memory[op2] = cycles_completed
            temp.append(op2)

        # re-populate the queue if finished.
        if not queue:
            if not temp:
                break
            else:
                queue = temp
                temp = []
                cycles_completed += 1

    return str(memory.get((bigger, smaller), 'impossible'))


def solution3(m, f):
    m, f = int(m), int(f)
    return helper3(*((m, f) if m < f else (f, m)))


def helper4(smaller, bigger):
    memory = {(1, 1): 0}

    cycles_completed = 1
    queue = [(1, 1), ]
    temp = []
    while queue:
        bombs = queue.pop()
        a, b = bombs[0], bombs[1]

        if a <= bigger and b <= smaller:
            op1 = (a + b, a if a > b else b)
            op2 = (a + b, b if a > b else a)

            if op1 in memory and memory.get(op1) <= cycles_completed:
                # do nothing? quit somehow?
                pass
            else:
                # update memory and continue.
                memory[op1] = cycles_completed
                temp.append(op1)

            if op2 in memory and memory.get(op2) <= cycles_completed:
                # do nothing? quit somehow?
                pass
            else:
                # update memory and continue.
                memory[op2] = cycles_completed
                temp.append(op2)

        # re-populate the queue if finished.
        if not queue:
            if not temp:
                break
            else:
                queue = temp
                temp = []
                cycles_completed += 1

    return str(memory.get((bigger, smaller), 'impossible'))


def solution4(m, f):
    m, f = int(m), int(f)
    return helper4(*((m, f) if m < f else (f, m)))


def helper5(smaller, bigger):
    cycles_completed = 0
    queue = [(1, 1), ]
    temp = []
    while queue:
        bombs = queue.pop()
        a, b = bombs[0], bombs[1]

        if a == bigger and b == smaller:
            return str(cycles_completed)
        elif a == bigger:
            continue
        # elif b == smaller:
        #     diff = bigger - b
        #     if diff % b == 0:
        #         return str(cycles_completed + (diff / b))
        elif a <= bigger and b <= smaller:
            op1 = (a + b, a if a > b else b)
            op2 = (a + b, b if a > b else a)
            if op1 != op2:
                temp.append(op1)
            temp.append(op2)

        # re-populate the queue if finished.
        if not queue:
            if not temp:
                break
            else:
                queue = temp
                temp = []
                cycles_completed += 1
    return 'impossible'


def solution5(m, f):
    m, f = int(m), int(f)
    return helper5(*((m, f) if m < f else (f, m)))


def helper6(m, f):
    """work bottom up."""
    cycles_completed = 0
    smaller, larger = (m, f) if m < f else (f, m)
    iterations = 0

    while smaller >= 1 and larger >= 1:
        iterations += 1
        if smaller == 1 and larger == 1:
            print str(iterations)
            return str(cycles_completed)
        elif larger // smaller > 1:
            times_smaller_fits_into_larger = (larger // smaller) - 1
            larger -= times_smaller_fits_into_larger * smaller
            cycles_completed += times_smaller_fits_into_larger
        else:
            a, b = larger - smaller, smaller
            larger, smaller = (a, b) if a > b else (b, a)
            cycles_completed += 1

    print str(iterations)
    return 'impossible'


def solution6(m, f):
    m, f = int(m), int(f)
    return helper6(m, f)


if __name__ == '__main__':

    # print solution6(str(10 ** 50 - 1), str(20 ** 49))
    # print solution6('13', '21')
    # exit(0)

    io = {
        ('4', '7'): '4',
        ('8', '3'): '4',
        ('8', '13'): '5',
        ('2', '1'): '1',
        (str(10 ** 6), '1'): str(10 ** 6 - 1),
        (str(10 ** 6 + 1), '2'): '500001',
        (str(10 ** 20 + 1), '20000'): '5000000000019999',
        (str(10 ** 50 - 1), str(20 ** 49)): '71054273576010018587225016748496770',
        (str(10 ** 2), str(10 ** 2)): 'impossible',
        ('2', '4'): 'impossible',
    }
    for solution in [solution6, solution5, solution4, solution3, solution2, solution1]:
        try:
            start = datetime.now()
            for i, o in io.iteritems():
                # print '{} --> {}: {}'.format(solution.__name__, i, solution(*i))
                assert solution(*i) == o
        except (RuntimeError, AssertionError):
            print "{} couldn't handle the stress test".format(solution.__name__)
        else:
            elapsed = (datetime.now() - start)
            print 'total time for {}: {}ms'.format(solution.__name__, elapsed.total_seconds()*1000)
