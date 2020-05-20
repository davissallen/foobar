import numpy as np

MAX_CASE = 10**8
SQUARE_ROOT_TWO = 2 ** 0.5

if __name__ == '__main__':
    i = long(1)
    output = long(SQUARE_ROOT_TWO)
    # f = open('generated_cases.csv', 'w')
    pct = 0
    while i < MAX_CASE:
        if i % (MAX_CASE / 100) == 0:
            pct += 1
            print '{}% complete'.format(pct)
        # f.write('{}\n'.format(output))
        i += 1
        if i >= 93222357:
            pass
        output += long(i * SQUARE_ROOT_TWO)
    # f.close()

