
filename = "input.txt"
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

def move(i, e, debug=False):
    y, x = e
    pos = None

    ADJACENT = {
        'NW': (y-1,x-1),
        'N':  (y-1,x),
        'NE': (y-1,x+1),
        'E':  (y,x+1),
        'SE': (y+1,x+1),
        'S':  (y+1,x),
        'SW': (y+1,x-1),
        'W':  (y,x-1),
    }
    _adjacent = list()
    for p in ADJACENT.values():
        if p in elves:
            _adjacent.append(p)

    if debug: print('  Adjacent:', _adjacent)
    if _adjacent:
        # directions
        DIRECTIONS = {
            "north": [ADJACENT['NW'], ADJACENT['N'], ADJACENT['NE']],
            "south": [ADJACENT['SW'], ADJACENT['S'], ADJACENT['SE']],
            "west":  [ADJACENT['NW'], ADJACENT['W'], ADJACENT['SW']],
            "east":  [ADJACENT['NE'], ADJACENT['E'], ADJACENT['SE']],
        }
        _directions = ["north", "south", "west", "east"]

        # pick a direction
        len_d = len(_directions)
        d = i % len_d
        for _ in range(len_d):
            if pos: break
            if d >= len_d:
                d -= len_d

            _direction = _directions[d]
            _valid = list()
            for p in DIRECTIONS[_direction]:
                if p in _adjacent:
                    break
                else:
                    _valid.append(p)
            if debug: print(f'  {_direction.title()}', _valid)
            if len(_valid) == 3:
                pos = _valid[1]
                break
            d += 1

    return pos

def run(start=0, end=None):
    i = start
    while True:
        if i == end:
            break
        _elves = dict()
        if debug: print(f'\nRound {i+1}, first half')
        for e in elves:
            if debug: print(f'Elf {e}')
            np = move(i, e, debug)
            if np:
                _elves.setdefault(np, list()).append(e)

        if debug: print(f'\nRound {i+1}, second half')
        moved = 0
        for e in _elves:
            if len(_elves[e]) == 1:
                st = _elves[e][0]
                if debug: print(f'  Move: {st} -> {e}')
                del elves[st]
                elves[e] = True
                moved += 1

        i += 1
        if debug:
            if i in [1,2,3,4,5,10]:
                print()
                _print(text=f'== End of Round {i} ==')
        if not moved:
            if debug: print(f'Round {i}, elves cant move!')
            break

    return i


debug = False
if debug: _print(text='== Initial State ==')

# part 1
# count unoccupied tiles in minimum rectangle
# after 10 rounds

end = run(end=10)
e = len(elves)
_y, _x = map(list, zip(*elves))
_y.sort()
_x.sort()
height = _y[-1] - _y[0] + 1
width = _x[-1] - _x[0] + 1
area = height * width
print("part1:", area - e)

# part 2
# continue from end of part 1
# and run until no more movement

end = run(start=end, end=None)
print("part2:", end)