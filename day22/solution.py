
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

pos = (0, rows[0][0])
path = dict()
heading = 0
count = 0
number = ''

def move(n):
    global pos

    if n <= 0:
        return
        
    print(f'Position {pos}')
    print(f'Heading {HEADINGS[heading][0]}')
    print(f'Moving {n} spaces')

    i = 1
    steps = list()
    movement = HEADINGS[heading][-1]
    ny = pos[0] + movement[0]
    nx = pos[1] + movement[1]
    npos = (ny, nx)
    while i <= int(number):
        # move to next position
        try:
            print("*", npos, grid[npos])
            if grid[npos] != '.':
                # stop!
                break
            else:
                path.setdefault(pos, list()).append(HEADINGS[heading][-2])
                pos = npos
                steps.append(pos)
                movement = HEADINGS[heading][-1]
                ny = pos[0] + movement[0]
                nx = pos[1] + movement[1]
                npos = (ny, nx)
                i += 1

        # wrap around
        except KeyError:
            print(f'Wrapping around the {HEADINGS[heading][0]} edge')
            # east
            if heading == 0:
                npos = (ny, rows[ny][0])
            # west
            elif heading == 180:
                npos = (ny, rows[ny][1])
            # north
            elif heading == 90:
                for _y in range(len(rows)-1, -1, -1):
                    print("N", _y, nx, rows[_y])
                    if nx in range(rows[_y][0], rows[_y][1]+1):
                        npos = (_y, nx)
                        break
            # south
            elif heading == 270:
                for _y in range(len(rows)):
                    print("S", _y, nx, rows[_y])
                    if nx in range(rows[_y][0], rows[_y][1]+1):
                        npos = (_y, nx)
                        break

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

