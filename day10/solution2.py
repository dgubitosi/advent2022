
_op = {
    'noop': 1,
    'addx': 2,
}

x = 1
cycle = 0

_width = 40
_height = 6
screen = [[' ']*_width for r in range(_height)]

with open('input.txt') as f:
    for line in f:
        line = line.strip().split(' ')
        op = line[0]
        _cycles = _op[op]

        for c in range(_cycles):
            cycle += 1
            row, pos = divmod(cycle, _width)
            pos -= 1

            sprite = [x-1, x, x+1]
            #print(cycle, (row, pos), sprite)
            if pos in sprite:
                #print('WRITE', (row, pos))
                # off screen?
                if 0 <= row < _height and 0 <= pos < _width:
                    screen[row][pos] = '#'

            # end of the op
            # c is zero offset
            if c + 1 == _cycles:
                if op == 'addx':
                    value = int(line[1])
                    x += value

for row in screen:
    print(''.join(row))
