
_x = set()
_y = set()
_z = set()
cubes = list()
with open("input.txt") as f:
    for line in f:
        p = (x, y, z) = [int(i) for i in line.strip().split(',', 3)]
        _x.add(x)
        _y.add(y)
        _z.add(z)
        cubes.append(p)

adjacent = dict()
for i in range(len(cubes)):
    a = cubes[i]
    adjacent[i] = list()
    for j in range(len(cubes)):
        if i == j:
            continue
        b = cubes[j]
        diff = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
        if diff == 1:
            print(f'adjacent: {i}:{cubes[i]} and {j}:{cubes[j]}')
            adjacent[i].append(j)

total = 0
for a in adjacent:
    sides = 6
    sides -= len(adjacent[a])
    total += sides
print()
print("part1:", total)
print()
print()

_x = sorted(list(_x))
_y = sorted(list(_y))
_z = sorted(list(_z))

print(_x)
print(_y)
print(_z)

planes = list()
row = [0]*(_x[-1]+1)
for z in range(0, _z[-1]+1):
    planes.append([row[:] for i in range(_y[-1]+1)])
    for c in cubes:
        if z == c[2]:
            planes[c[2]][c[1]][c[0]] = 1

for i, z in enumerate(planes):
    print()
    print("z-plane:", i)
    for y in z:
        row = ''
        for x in y:
            if x:
                row += '#'
            else:
                row += '.'
        print(row)
    print("z-plane:", i)

