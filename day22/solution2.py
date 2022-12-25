
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

FINDEX = {
    (0,2): 1,
    (0,1): 2,
    (1,1): 3,
    (2,1): 4,
    (2,0): 5,
    (3,0): 6,
}

FACES = {
    1: {
        'N': (6, 'N'),
        'S': (3, 'W'),
        'E': (4, 'W'),
        'W': (2, 'W'),
    },
    2: {
        'N': (6, 'E'),
        'S': (3, 'S'),
        'E': (1, 'E'),
        'W': (5, 'E'),
    },
    3: {
        'N': (2, 'N'),
        'S': (4, 'S'),
        'E': (1, 'N'),
        'W': (5, 'S'),
    },
    4: {
        'N': (3, 'N'),
        'S': (6, 'W'),
        'E': (1, 'W'),
        'W': (5, 'W'),
    },
    5: {
        'N': (3, 'E'),
        'S': (6, 'S'),
        'E': (4, 'E'),
        'W': (2, 'E'),
    },
    6: {
        'N': (5, 'N'),
        'S': (1, 'S'),
        'E': (4, 'N'),
        'W': (2, 'S'),
    },
}

# draw grid with path
# now in technicolor!
def draw(msec=0):
    import os
    import time
    from termcolor import colored

    os.system('clear')
    for y in range(len(rows)):
        row = ''
        for x in range(x_max):
            p = (y, x)
            if p in grid:
                if p == pos:
                    row += colored(' ', 'yellow', attrs=["reverse", "bold"])
                elif p in visited:
                    row += colored(visited[p][-1], 'green', attrs=["reverse"])
                else:
                    row += grid[p]
            else:
                row += ' '
        print(row)

    if msec > 0:
        time.sleep(1*msec/1000)

def move(n):
    global pos
    global heading

    if n <= 0:
        return

    if debug:
        print(f'Moving {n} spaces')
        print(f'Position {pos}')
        print(f'Heading {heading} {HEADINGS[heading][0]}')

    pface = FINDEX[tuple(v//50 for v in pos)]
    movement = HEADINGS[heading][-1]
    npos = tuple(a + b for a, b in zip(pos, movement))
    nh = heading

    steps = list()
    for i in range(n):
        if npos not in grid:
            direction = HEADINGS[heading][0]
            d = direction[0]
            nf, nd = FACES[pface][d]
            nh = DIR[nd]
            if debug: print(f'Wrapping around the {direction} edge, face {pface} to {nf}')
            tr = f'{pface}:{nf}'
            y, x = pos
            transform = {
                "1:3": (x-50, 99),          # y off grid
                "1:4": (149-y, 99),         # x off grid
                "1:6": (199, x-100),        # y off grid
                "2:5": (149-y, 0),          # x off grid
                "2:6": (x+100, 0),          # y off grid
                "3:1": (49, y+50),          # x off grid
                "3:5": (100, y-50),         # x off grid
                "4:1": (149-y, 149),        # x off grid
                "4:6": (x+100, 49),         # y off grid
                "5:2": (149-y, 50),         # x off grid
                "5:3": (50+x, 50),          # y off grid
                "6:1": (0, x+100),          # y off grid
                "6:2": (0, y-100),          # x off grid
                "6:4": (149, y-100),        # x off grid
            }
            npos = transform[tr]
            if debug: 
                print(f'transform({tr}): {pface}:{pos} -> {nf}:{npos}, direction {d} -> {nd}, heading {heading} -> {nh}')

        nface = FINDEX[tuple(v//50 for v in npos)]
        if debug: print(f'* face:{pface}:{pos} -> face:{nface}:{npos} {grid[npos]}')

        if grid[npos] != '.':
            # stop!
            break

        visited.setdefault(pos, list()).append(HEADINGS[heading][-2])
        steps.append(npos)
        pos = npos
        heading = nh
        pface = FINDEX[tuple(v//50 for v in pos)]
        movement = HEADINGS[heading][-1]
        npos = tuple(a + b for a, b in zip(pos, movement))
        #draw(100)

    # record path
    path.extend(steps)

    # return how many spaces we've moved
    i = len(steps)
    if debug:
        print(steps)
        print(f'Moved {i} spaces')
    return i

# starting position and heading
pos = (0, rows[0][0])
heading = 0

visited = dict()
path = [pos]
debug = True

count = 0
number = ''
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
            if heading >= 360:
                heading -= 360
        else:
            continue
        if debug:
            print(f'\nTurning {d}, heading {heading} {HEADINGS[heading][0]}\n')

# last position
count += move(int(number))
visited.setdefault(pos, list()).append(HEADINGS[heading][-2])

#draw()
#print(visited)
#print(path)

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

