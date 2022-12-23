
filename = "test.txt"
elves = dict()
with open(filename) as f:
    y = 0
    for line in f:
        line = line.strip()
        x = 0
        for c in line:
            if c == '#':
                elves[(y, x)] = True
            x += 1
        y += 1

def _print(text='', extra=2):
    if text: print(text)

    _y, _x = map(list, zip(*elves))
    _y.sort()
    _x.sort()
    _y_range = (_y[0]-extra, _y[-1]+1+extra)
    _x_range = (_x[0]-extra, _x[-1]+1+extra)
    for y in range(*_y_range):
        row = ''
        for x in range(*_x_range):
            p = (y, x)
            if p in elves and elves[p]:
                row += '#'
            else:
                row += '.'
        print(row)


def move(e, debug=False):
    y, x = e
    np = None

    # directions
    DIRECTIONS = {
        "north": [(y-1,x-1), (y-1,x), (y-1,x+1)], # n = y-1
        "south": [(y+1,x-1), (y+1,x), (y+1,x+1)], # s = y+1
        "west":  [(y-1,x-1), (y,x-1), (y+1,x-1)], # w = x-1
        "east":  [(y-1,x+1), (y,x+1), (y+1,x+1)], # e = x+1
    }
    _directions = ["north", "south", "west", "east"]

    # pick a direction
    len_d = len(_directions)
    d = i % len_d
    np = None
    for _ in range(len_d):
        if np: break
        if d >= len_d:
            d -= len_d

        _direction = _directions[d]
        if debug: print(f'Testing {_direction}:')
        valid = list()
        for p in DIRECTIONS[_direction]:
            if p in elves:
                continue
            else:
                valid.append(p)
        if debug: print(valid)
        if len(valid) == 3:
            np = valid[1]
            break
        d += 1

    return np

debug = True
_print(text='== Initial State ==')
i = 0
while i < 2:
    _elves = dict()
    for e in elves:
        if debug: print(f'Elf {e}')
        np = move(e, debug)
        if np:
            _elves.setdefault(np, list()).append(e)

    for e in _elves:
        if len(_elves[e]) == 1:
            st = _elves[e][0]
            if debug: print(f'Move {st} to {e}')
            del elves[st]
            elves[e] = True

    i += 1
    if i in [1,2,3,4,5,10]:
        print()
        _print(text=f'== End of Round {i} ==')

