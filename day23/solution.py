
filename = "test.txt"
x_min = 0
x_max = 0
y_min = 0
y_max = 0
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
        x_max = max(x_max, x)
        y += 1
    y_max = y

def _print(text=''):
    if text: print(text)
    for y in range(y_min, y_max+1):
        row = ''
        for x in range(x_min, x_max+1):
            p = (y, x)
            if p in elves and elves[p]:
                row += '#'
            else:
                row += '.'
        print(row)

_print('== Initial State ==')
i = 0
while i < 2:
    _elves = dict()
    for e in elves:
        print(f'Elf {e}')
        y, x = e

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
            print(f'Testing {_direction}:')
            valid = list()
            for p in DIRECTIONS[_direction]:
                if p in elves:
                    continue
                else:
                    valid.append(p)
            print(valid)
            if len(valid) == 3:
                np = valid[1]
                break
            d += 1

        # cant move
        if np:
            _elves.setdefault(np, list()).append(e)

    for e in _elves:
        if len(_elves[e]) == 1:
            st = _elves[e][0]
            print(f'Move {st} to {e}')
            del elves[st]
            elves[e] = True
            y, x = e
            y_min = min(y, y_min)
            y_max = max(y, y_max)
            x_min = min(x, x_min)
            x_max = max(x, x_max)

    i += 1
    if i in [1,2,3,4,5,10]:
        print()
        _print(f'== End of Round {i} ==')

