
filename = "input.txt"
grid = dict()
rows = list()
moves = ''
x_max = 0
with open(filename) as f:
    y = 0
    for line in f:
        # grid
        if '.' in line:
            line = line.rstrip()
            row = list()
            x = 0
            for c in line:
                if c != ' ':
                    row.append(x)
                    grid[(y, x)] = c
                x += 1
            x_max = max(x_max, row[-1])
            rows.append([row[0], row[-1]])
            y += 1
        # moves
        else:
            moves = line.strip()


HEADINGS = {
    0:   ["East",  0, ">", ( 0,  1)], # right
    90:  ["North", 3, "^", (-1,  0)], # up
    180: ["West",  2, "<", ( 0, -1)], # left
    270: ["South", 1, "v", ( 1,  0)], # down
}

DIR = {
    'N': 90,
    'S': 270,
    'E': 0,
    'W': 180,
}

FACES = {
    1: { 
        'y': [0, 49],
        'x': [100, 149],
        'N': (6, 'N'),
        'S': (3, 'W'),
        'E': (4, 'W'),
        'W': (2, 'W'),
    },
    2: { 
        'y': [0, 49],
        'x': [50, 99],
        'N': (6, 'E'), 
        'S': (3, 'S'),
        'E': (1, 'E'), 
        'W': (5, 'E'),
    },
    3: { 
        'y': [50, 99],
        'x': [50, 99],
        'N': (2, 'N'),
        'S': (4, 'S'),
        'E': (1, 'N'),
        'W': (5, 'S'),
    },
    4: {
        'y': [100, 149],
        'x': [50, 99],
        'N': (3, 'N'),
        'S': (6, 'W'),
        'E': (1, 'W'),
        'W': (5, 'W'),
    },
    5: {
        'y': [100, 149],
        'x': [0, 49],
        'N': (3, 'E'),
        'S': (6, 'S'),
        'E': (4, 'E'),
        'W': (2, 'E'),
    },
    6: {
        'y': [150, 199],
        'x': [0, 49],
        'N': (5, 'N'),
        'S': (1, 'S'),
        'E': (4, 'N'),
        'W': (2, 'S'),
    },
}

pos = (0, rows[0][0])
path = dict()
heading = 0
count = 0
number = ''

def move(n):
    global pos
    global heading

    if n <= 0:
        return
        
    print(f'Position {pos}')
    print(f'Heading {HEADINGS[heading][0]}')
    print(f'Moving {n} spaces')

    py, px = pos
    movement = HEADINGS[heading][-1]
    ny = py + movement[0]
    nx = px + movement[1]
    npos = (ny, nx)

    i = 1
    steps = list()
    while i <= int(number):
        # move to next position
        try:
            face = 0
            for f in FACES:
                fy = (FACES[f]['y'][0], FACES[f]['y'][1]+1)
                fx = (FACES[f]['x'][0], FACES[f]['x'][1]+1)
                if py in range(*fy) and px in range(*fx):
                    face = f
                    break
            assert 1 <= face <= 6
            print(f'* face {face}:{pos} -> {npos} {grid[npos]}')

            if grid[npos] != '.':
                # stop!
                break
            else:
                path.setdefault(pos, list()).append(HEADINGS[heading][-2])
                steps.append(npos)
                pos = npos
                py, px = pos
                movement = HEADINGS[heading][-1]
                ny = py + movement[0]
                nx = px + movement[1]
                npos = (ny, nx)
                i += 1

        # wrap around
        except KeyError:
            _direction = HEADINGS[heading][0]
            _d = _direction[0]
            nf, nd = FACES[face][_d]
            nh = DIR[nd]
            print(f'Wrapping around the {_direction} edge, face {face} to {nf}')
            tr = f'{face}:{nf}'
            y, x = npos
            transform = {
                "1:3": (x-50, 99),          # y off grid
                "1:4": (100+abs(y-49), 99), # x off grid
                "1:6": (199, x-100),        # y off grid
                "2:5": (100+abs(y-49), 0),  # x off grid
                "2:6": (x+100, 0),          # y off grid
                "3:1": (49, y+50),          # x off grid
                "3:5": (100, y-50),         # x off grid
                "4:1": (149-y, 149),        # x off grid
                "4:6": (x+100, 49),         # y off grid
                "5:2": (abs(149-y), 50),    # x off grid
                "5:3": (50+x, 50),          # y off grid
                "6:1": (0, x+100),          # y off grid
                "6:2": (0, y-100),          # x off grid
                "6:4": (149, y-100),        # x off grid
            }
            tpos = transform[tr]
            print(f'transform({tr}): {face}:{npos} -> {nf}:{tpos}, {_d} -> {nd}, heading {nh}')
            npos = tpos
            heading = nh

    # how many spaces we've moved
    i -= 1
    assert i == len(steps)
    print(steps)
    print(f'Moved {i} spaces')
    return i

for c in moves:
    if c.isdigit():
        number += c
    else:
        count += move(int(number))

        # reset the number collector
        number = ''

        # change direction
        d = ''
        if c == 'R':
            d = 'Right'
            heading -= 90
            if heading < 0:
                heading += 360
        elif c == 'L':
            d = 'Left'
            heading += 90
            if heading == 360:
                heading = 0
        else:
            continue
        print(f'Turning {d}, now heading {HEADINGS[heading][0]}\n')

# last position
count += move(int(number))
path.setdefault(pos, list()).append(HEADINGS[heading][-2])

#print(moves)
#print(path)

# draw grid with path
test = '''
for y in range(len(rows)):
    row = ''
    for x in range(x_max):
        p = (y, x)
        if p in grid:
            if p in path:
                row += path[p][-1]
            else:
                row += grid[p]
        else:
            row += ' '
    print(row)
'''

print()
print()
print("Final Position:", pos)
print("Final Heading:", HEADINGS[heading][0])
y, x = pos
y += 1
x += 1
print("- Row:", y)
print("- Col:", x)
password = 1000*y + 4*x + HEADINGS[heading][1]
print("part1:", password)

