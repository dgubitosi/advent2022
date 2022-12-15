
def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

sensors = dict()
beacons_at_y = set()

options = {
    'test.txt': 10,
    'input.txt': 2000000
}

name = 'input.txt'
y = options[name]

x_ranges = list()
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
        sensors.setdefault(s, dict())
        sensors[s]['b'] = d

        # collect the beacons at row y
        if by == y:
            beacons_at_y.add(b)

        # for y, solve for x
        # d = abs(x-sx) + abs(y-sy)
        # abs(x-sx) = dist - abs(y-sy)
        x1 = sx - (d - abs(y-sy))
        x2 = sx + (d - abs(y-sy))
        xr = (min(x1, x2), max(x1, x2))

        # check sensors
        dd1 = dist(s, (xr[0],y))
        dd2 = dist(s, (xr[1],y))
        if dd1 <= d and dd2 <= d:
            print(f'sensor at {s}, d={d}, y={y}, x-range={xr}')
            x_ranges.append(xr)

            # list of x ranges per sensor
            # that continually is reduced
            if len(x_ranges) > 1:
                x_ranges.sort()
                i = 1
                while i < len(x_ranges):
                    print(x_ranges)
                    a = x_ranges[i-1]
                    b = x_ranges[i]
                    print(f'x[{i-1}]={a}, x[{i}]={b}')
                    # overlaps or adjacent
                    if a[0] <= b[0] <= a[1]+1:
                        n = (a[0], max(a[1], b[1]))
                        print(f'.. reduced to {n}')
                        x_ranges[i-1] = n
                        del x_ranges[i]
                    else:
                        i += 1
                print()

not_present = 0
for x in x_ranges:
    not_present += x[1] - x[0] + 1
print("part1:", not_present - len(beacons_at_y))