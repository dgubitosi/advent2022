

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
    *nest, element = index
    layer = source
    for i in nest:
        layer = layer[i]
    layer[element] = [layer[element]]
    return source

def equals(left, right):

    l_index = [0]
    r_index = [0]

    l = _get(left, l_index)
    r = _get(right, r_index)

    correct = False
    while True:

        type_l = [type(l) is list, type(l) is int]
        value_l = int(''.join(str(int(pos)) for pos in type_l), 2)
        type_r = [type(r) is list, type(r) is int]
        value_r = int(''.join(str(int(pos)) for pos in type_r), 2)

        print(" ", l_index, l, type_l, value_l)
        print(" ", r_index, r, type_r, value_r)

        # both ran out so try next position
        if value_l == value_r == 0:
            print("  .. left and right are none")
            l_index.pop(-1)
            l_index[-1] += 1
            r_index.pop(-1)
            r_index[-1] += 1
        # left ran out of items first
        elif value_l == 0:
            print("  .. left is none")
            correct = True
            break
        # right ran out of items first
        elif value_r == 0:
            print("  .. right is none")
            break
        # both are integers
        elif value_l == value_r == 1:
            print("  .. left and right are int")
            if l == r:
                l_index[-1] += 1
                r_index[-1] += 1
            elif l < r:
                correct = True
                break
            else:
                break
        # both are lists
        elif value_l == value_r == 2:
            print("  .. left and right are list")
            l_index.append(0)
            r_index.append(0)
        # type mismatch, left is int
        elif value_l == 1:
            print("  .. mismatch, left is int, right is list")
            left = _replace(left, l_index)
            l_index.append(0)
            r_index.append(0)
        # type mismatch right is int
        elif value_r == 1:
            print("  .. mismatch, right is int, left is list")
            right = _replace(right, r_index)
            l_index.append(0)
            r_index.append(0)

        # walk deeper
        l = _get(left, l_index)
        r = _get(right, r_index)

    return correct

signals = []
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        if line:
            signals.append(eval(line))

pair = 0
_sum = 0
for i in range(0, len(signals), 2):
    pair += 1
    left = signals[i]
    right = signals[i+1]

    print(f'== Pair {pair} ==')
    print(left)
    print(right)
    print()

    _is = "is"
    if equals(left, right):
        _sum += pair
    else:
        _is += " not"
    print()
    print(f"Pair {pair} {_is} in the right order")
    print()

print("Sum", _sum)
