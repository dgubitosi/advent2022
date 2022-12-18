
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
            #print(f'adjacent: {i}:{cubes[i]} and {j}:{cubes[j]}')
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

def _print():
    icons = ['~', '.', '#']
    for i, z in enumerate(planes):
        print()
        print("z-plane:", i)
        row = '+'
        for j in range(len(z[0])):
            row += f'{str(j)[-1]}'
        print(row)
        for j, y in enumerate(z):
            row = f'{str(j)[-1]}'
            for x in y:
                row += icons[x+1]
            print(row)
        print("z-plane:", i)

planes = list()
row = [-1]*(_x[-1]+1)
for z in range(0, _z[-1]+1):
    planes.append([row[:] for i in range(_y[-1]+1)])
    for c in cubes:
        if z == c[2]:
            planes[c[2]][c[1]][c[0]] = 1

# z = 0 -> max
for i in range(len(planes)):
    for j in range(len(planes[z])):
        for k in range(len(planes[z][y])):
            if planes[i][j][k] < 0:
                # outer plane
                if i == 0:
                    planes[i][j][k] = 0
                # otherwise check the adjacent plane
                else:
                    if planes[i-1][j][k] == 0:
                        planes[i][j][k] = 0

# y = 0 -> max
for i in range(len(planes)):
    for j in range(len(planes[z])):
        for k in range(len(planes[z][y])):
            if planes[i][j][k] < 0:
                # outer plane
                if j == 0:
                    planes[i][j][k] = 0
                # otherwise check the adjacent plane
                else:
                    if planes[i][j-1][k] == 0:
                        planes[i][j][k] = 0

# x = 0 -> max
for i in range(len(planes)):
    for j in range(len(planes[z])):
        for k in range(len(planes[z][y])):
            if planes[i][j][k] < 0:
                # outer plane
                if k == 0:
                    planes[i][j][k] = 0
                # otherwise check the adjacent plane
                else:
                    if planes[i][j][k-1] == 0:
                        planes[i][j][k] = 0

# z = max -> 0
for i in range(len(planes)-1, -1, -1):
    for j in range(len(planes[z])):
        for k in range(len(planes[z][y])):
            if planes[i][j][k] < 0:
                # outer plane
                if i == len(planes)-1:
                    planes[i][j][k] = 0
                # otherwise check the plane below
                else:
                    if planes[i+1][j][k] == 0:
                        planes[i][j][k] = 0

# y = max -> 0
for i in range(len(planes)):
    for j in range(len(planes[z])-1, -1, -1):
        for k in range(len(planes[z][y])):
            if planes[i][j][k] < 0:
                # top plane
                if j == len(planes[z])-1:
                    planes[i][j][k] = 0
                # otherwise check the adjacent plane
                else:
                    if planes[i][j+1][k] == 0:
                        planes[i][j][k] = 0
# x = max -> 0
for i in range(len(planes)):
    for j in range(len(planes[z])):
        for k in range(len(planes[z][y])-1, -1, -1):
            if planes[i][j][k] < 0:
                # otherwise check the adjacent plane
                if k == len(planes[z][y])-1:
                    planes[i][j][k] = 0
                # otherwise check the plane below
                else:
                    if planes[i][j][k+1] == 0:
                        planes[i][j][k] = 0

_print()

