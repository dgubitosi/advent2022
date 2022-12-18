
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

def adjacency(_list):
    adjacent = dict()
    for i in range(len(_list)):
        a = _list[i]
        adjacent[i] = list()
        for j in range(len(_list)):
            if i == j:
                continue
            b = _list[j]
            diff = abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
            if diff == 1:
                #print(f'adjacent: {i}:{cubes[i]} and {j}:{cubes[j]}')
                adjacent[i].append(j)
    return adjacent

adjacent = adjacency(cubes)
area = 0
for a in adjacent:
    sides = 6
    sides -= len(adjacent[a])
    area += sides

print("part1:", area)

_x = sorted(list(_x))
_y = sorted(list(_y))
_z = sorted(list(_z))

#print(_x)
#print(_y)
#print(_z)

planes = list()
row = [-1]*(_x[-1]+1)
for z in range(0, _z[-1]+1):
    planes.append([row[:] for i in range(_y[-1]+1)])
    for c in cubes:
        if z == c[2]:
            planes[c[2]][c[1]][c[0]] = 1

# start the corner as exterior space
planes[0][0][0] = 0
start = (0,0,0)

visited = set()
to_visit = list()
to_visit.append(start)

#print("walking...")
while to_visit:
    n = to_visit.pop(0)
    #print(n)
    if n not in visited:
        visited.add(n)
    else:
        continue

    i, j, k = n
    if planes[i][j][k] == 0:
        # find all adjacent points
        neighbors = list()
        if i > 0:
            neighbors.append((i-1,j,k))
        if i < len(planes)-1:
            neighbors.append((i+1,j,k))
        if j > 0:
            neighbors.append((i,j-1,k))
        if j < len(planes[z])-1:
            neighbors.append((i,j+1,k))
        if k > 0:
            neighbors.append((i,j,k-1))
        if k < len(planes[z][y])-1:
            neighbors.append((i,j,k+1))
        for n in neighbors:
            to_visit.append(n)
            z, y, x = n
            if planes[z][y][x] < 0:
                planes[z][y][x] = 0

#_print()

interior = list()
for i in range(len(planes)):
    for j in range(len(planes[z])):
        for k in range(len(planes[z][y])):
            if planes[i][j][k] < 0:
                interior.append((i,j,k))

adjacent = adjacency(interior)
space = 0
for a in adjacent:
    sides = 6
    sides -= len(adjacent[a])
    space += sides

print("part2:", area - space, "... interior area:", space)

