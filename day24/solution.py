
dydx = {
    ( 0,  1): '>', # right
    ( 0, -1): '<', # left
    (-1,  0): '^', # up
    ( 1,  0): 'v', # down
}
_dir = dict({v: k for k, v in dydx.items()})

y_max = 0
x_max = 0
blizzards = dict()
blizzards[0] = dict()

filename = 'input.txt'
with open(filename) as f:
    y = 0
    for line in f:
        for x, c in enumerate(line.strip()):
            x_max = x
            pos = (y, x)
            if c in _dir:
                blizzards[0].setdefault(pos, list()).append(_dir[c])
        y += 1
    y_max = y - 1

# assume a square valley
# walls are the outside edges
# except for the start and end
start = (0, 1)
end = (y_max, x_max-1)
#print(start, end)

def draw(t, p):
    print(f'== time: {t} ==')
    for y in range(y_max+1):
        row = ''
        for x in range(x_max+1):
            pos = (y, x)
            b = 0
            if is_wall(pos):
                row += '#'
            elif pos == p:
                row += 'E'
            elif pos in blizzards[t]:
                b = len(blizzards[t][pos])
                if b > 1:
                    row += str(b)
                else:
                    row += dydx[blizzards[t][pos][0]]
            else:
                row += '.'
        print(row)
    print()

def is_wall(pos):
    y, x = pos
    if pos in [start, end]:
        return False
    elif y == 0 or y == y_max:
        return True
    elif x == 0 or x == x_max:
        return True
    return False

# current state as (time, position)
state = (0, start)
to_evaluate = [state]

# keep track of all evaluated states
_states = set()

while to_evaluate:
    state = to_evaluate.pop(0)
    if state in _states:
        continue
    _states.add(state)

    #draw(*state)

    t, pos = state
    if pos == end:
        print(f'End at time: {t}')
        break

    # move blizzards to time t+1
    # if not already calculated at time t+1
    if not t+1 in blizzards:
        blizzards[t+1] = dict()
        for b in blizzards[t]:
            for d in blizzards[t][b]:
                n = tuple(a + b for a, b in zip(b, d))
                ny, nx = n
                # wrap around
                if is_wall(n):
                    wrap = {
                        ( 0,  1): (ny, 1),       # right > wrap to left edge
                        ( 0, -1): (ny, x_max-1), # left > wrap to right edge
                        (-1,  0): (y_max-1, nx), # up > wrap to bottom edge
                        ( 1,  0): (1, nx),       # down > wrap to top edge
                    }
                    n = wrap[d]
                blizzards[t+1].setdefault(n, list()).append(d)

    # stay here next turn?
    if pos not in blizzards[t+1]:
        to_evaluate.append((t+1, pos))

    # adjacent available tiles for next turn?
    for d in dydx:
        n = tuple(a + b for a, b in zip(pos, d))
        ny, nx = n
        if nx in range(0, x_max+1) and ny in range(0, y_max+1) and not is_wall(n) and n not in blizzards[t+1]:
            to_evaluate.append((t+1, n))

    # sort the list
    # ensures lowest times are at the front
    to_evaluate.sort()
