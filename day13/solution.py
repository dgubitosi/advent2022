

def _get(source, index):
    r = None
    try:
        item = source
        for i in index:
            r = item[i]
            item = r
    except:
        r = None
    return r

def _replace(source, index):
    # thank you 
    # https://stackoverflow.com/a/40245529/6274853
    *nest, element = index
    layer = source
    for i in nest:
        layer = layer[i]
    layer[element] = [layer[element]]
    return source

def correct(left, right, debug=False):

    l_index = [0]
    r_index = [0]

    l = _get(left, l_index)
    r = _get(right, r_index)

    _correct = False
    while True:

        type_l = [type(l) is list, type(l) is int]
        value_l = int(''.join(str(int(pos)) for pos in type_l), 2)
        type_r = [type(r) is list, type(r) is int]
        value_r = int(''.join(str(int(pos)) for pos in type_r), 2)

        if debug:
            print(" ", l_index, l, type_l, value_l)
            print(" ", r_index, r, type_r, value_r)

        # both ran out so try next position
        if value_l == value_r == 0:
            if debug: print("  .. left and right are none")
            l_index.pop(-1)
            l_index[-1] += 1
            r_index.pop(-1)
            r_index[-1] += 1
        # left ran out of items first
        elif value_l == 0:
            if debug: print("  .. left is none")
            _correct = True
            break
        # right ran out of items first
        elif value_r == 0:
            if debug: print("  .. right is none")
            break
        # both are integers
        elif value_l == value_r == 1:
            if debug: print("  .. left and right are int")
            # if equal advance to the next index
            if l == r:
                l_index[-1] += 1
                r_index[-1] += 1
            # good
            elif l < r:
                _correct = True
                break
            # bad
            else:
                break
        # both are lists
        elif value_l == value_r == 2:
            if debug: print("  .. left and right are list")
            l_index.append(0)
            r_index.append(0)
        # type mismatch, left is int
        elif value_l == 1:
            if debug: print("  .. mismatch, left is int, right is list")
            left = _replace(left, l_index)
            l_index.append(0)
            r_index.append(0)
        # type mismatch right is int
        elif value_r == 1:
            if debug: print("  .. mismatch, right is int, left is list")
            right = _replace(right, r_index)
            l_index.append(0)
            r_index.append(0)

        # walk deeper
        l = _get(left, l_index)
        r = _get(right, r_index)

    return _correct

signals = []
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            signals.append(eval(line))

# part1
pair = 0
_sum = 0
for i in range(0, len(signals), 2):
    pair += 1
    left = signals[i]
    right = signals[i+1]

    print(f'== Pair {pair} ==')
    print("Left", left)
    print("Right", right)
    print()

    _is = "is"
    if correct(left, right, debug=True):
        _sum += pair
    else:
        _is += " not"
    print()
    print(f"Pair {pair} {_is} in the right order")
    print()

print("Part1: sum:", _sum)
print()

# part2
_two = [[2]]
_six = [[6]]
packets = list()
packets.append(_two)
packets.append(_six)

for i in range(len(signals)):
    s = signals[i]
    _inserted = False
    for j in range(len(packets)):
        if correct(s, packets[j]):
            print(f'{i}: Inserting at pos {j}')
            packets.insert(j, s)
            _inserted = True
            break
    if not _inserted:
        print(f'{i}: Appending at pos {len(packets)}')
        packets.append(s)

print()
print("Part2: decoder key:", (packets.index(_two) + 1) * (packets.index(_six) + 1))
