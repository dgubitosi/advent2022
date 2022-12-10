
_op = {
    'noop': 1,
    'addx': 2,
}

_signal = {
    20: 0,
    60: 0,
    100: 0,
    140: 0,
    180: 0,
    220: 0,
}

x = 1
cycle = 0
_x = [(cycle, x)]

with open('input.txt') as f:
    done = False
    for line in f:
        line = line.strip().split(' ')
        op = line[0]
        _cycles = _op[op]
        for c in range(_cycles):
            cycle += 1
            if cycle in _signal:
                _signal[cycle] = cycle * x
                if cycle == max(_signal):
                    s = sum([_signal[i] for i in _signal])
                    print(s)
                    done = True
                    break
            # end of the op
            # c is zero offset
            if c + 1 == _cycles:
                if op == 'addx':
                    value = int(line[1])
                    x += value
                    _x.append((cycle, x))
        if done:
            break

#print(_signal)
#print(_x)

