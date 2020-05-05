import fractions


def solution(pegs):

    if not pegs or len(pegs) < 2:
        return [-1, -1]
    elif len(pegs) == 2:
        distance = pegs[1] - pegs[0]
        if distance < 3:
            return [-1, -1]
        else:
            first_gear = fractions.Fraction(2 * distance, 3)
            return [first_gear.numerator, first_gear.denominator]

    is_even_length = len(pegs) % 2 == 0

    first_gear = -pegs[0] + (1 if is_even_length else -1)*pegs[-1]

    for idx in xrange(1, len(pegs) - 1):
        first_gear += 2 * pegs[idx] * (-1 if idx % 2 == 0 else 1)

    numerator = first_gear * 2
    denominator = 3 if is_even_length else 1
    first_gear_radius = fractions.Fraction(numerator, denominator)

    # now that I know the first gear radius is, I need to make sure the other gears fit the constraints of:
    #   each radius >= 1

    if first_gear_radius < 1:
        return [-1, -1]

    current_radius = first_gear_radius
    for idx in xrange(0, len(pegs)-1):
        distance = pegs[idx+1] - pegs[idx]
        next_radius = distance - current_radius
        if next_radius < 1:
            return [-1, -1]
        current_radius = next_radius

    # finally, return the first gear radius
    return [first_gear_radius.numerator, first_gear_radius.denominator]


if __name__ == '__main__':
    assert solution([4, 30, 50]) == [12, 1]
    assert solution([4, 17, 50]) == [-1, -1]
    assert solution([1, 5, 9, 12]) == [2, 1]
    assert solution([1, 3]) == [-1, -1]
    assert solution([1, 4]) == [2, 1]
