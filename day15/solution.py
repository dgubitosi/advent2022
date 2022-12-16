
def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

sensors = dict()
beacons_at_y = set()

options = {
    'test.txt': [10, 20],
    'input.txt': [2000000, 4000000]
}

name = 'input.txt'
y = options[name][0]
y_range = options[name][1]
x_ranges = list()

def x_range(position, distance, y, debug=False):
    px, py = position
    # does the sensor area intersect the y row?
    if (py - distance) <= y <= (py + distance):
        # for y, solve for x
        # d = abs(x-sx) + abs(y-sy)
        # abs(x-sx) = d - abs(y-sy)
        # x = sx +/- (d - abs(y-sy))
        dy = distance - abs(y - py)
        xr = (px - dy, px + dy)
        if debug: print(f'sensor at {position}, d={distance}, y={y}, x-range={xr}')
        return xr
    return None

def squash(source, debug=False):
    if debug: print(f'squash: {source}')
    if len(source) < 2:
        return source
    # len(source) > 1
    _ranges = sorted(source)
    i = 1
    while i < len(_ranges):
        a = _ranges[i-1]
        b = _ranges[i]
        if debug: print(f'range[{i-1}]={a}, range[{i}]={b}')
        # overlaps or adjacent
        if a[0] <= b[0] <= a[1]+1:
            n = (a[0], max(a[1], b[1]))
            if debug: print(f'.. reduced to {n}')
            _ranges[i-1] = n
            del _ranges[i]
        else:
            i += 1
    return _ranges

with open(name) as f:
    for line in f:
        line = line.strip()
        s, b = line.split(":", 2)

        # sensor
        s = s.split()
        sx = int(s[2][2:-1])
        sy = int(s[3][2:])
        s = (sx, sy)

        # beason
        b = b.split()
        bx = int(b[4][2:-1])
        by = int(b[5][2:])
        b = (bx, by)

        # manhattan distance
        d = dist(s, b)
        sensors[s] = d

        # collect the beacons at row y
        if by == y:
            beacons_at_y.add(b)

        _x_range = x_range(s, d, y, debug=True)
        if _x_range:
            x_ranges.append(_x_range)

x_ranges = squash(x_ranges, debug=True)
print(x_ranges)

not_present = 0
for x in x_ranges:
    not_present += x[1] - x[0] + 1
print("part1:", not_present - len(beacons_at_y))
print()

# part2
# after optmizations, brute force now under 100 seconds
print('part2 starting ...')

import time
st = time.time()

for y in range(y_range):
    x_ranges.clear()
    if y and y % 100_000 == 0:
        et = time.time() - st
        print(f'{y} .. {et:.3f} s')

    for s in sensors:
        _x_range = x_range(s, sensors[s], y)
        if _x_range:
            x_ranges.append(_x_range)

    x_ranges = squash(x_ranges)
    if len(x_ranges) == 2:
        et = time.time() - st
        print(f'{y} .. {et:.3f} s')
        print(x_ranges)
        x = x_ranges[0][1] + 1
        if x != x_ranges[1][0] - 1:
            raise Exception('Barf!')
        print(f'position ({x}, {y})')
        print("part2:", x * 4000000 + y)
        break
