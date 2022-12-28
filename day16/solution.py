
class Valve(object):
    def __init__(self, name, rate=0, neighbors=list()):
        self.name = name
        self.rate = rate
        self.neighbors = neighbors

valves = dict()
non_zero = list()
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        line = line.split()
        v = line[1]
        r = int(''.join([i for i in line[4] if i.isdigit()]))
        if r > 0:
            non_zero.append(v)
        n = ''.join(line[9:]).split(',')
        valve = Valve(v, r, n)
        valves[v] = valve

def bfs(start):
    _inf = float('inf')
    to_visit = [(start, 0)]
    cost = {start: _inf}
    while to_visit:
        node, c = to_visit.pop(0)
        if c < cost[node]:
            cost[node] = c
            for neighbor in valves[node].neighbors:
                if neighbor not in cost:
                    cost[neighbor] = _inf
                nc = c + 1
                if nc < cost[neighbor]:
                    to_visit.append((neighbor, nc))
    return cost

# we only care about the non-zero valves
# find shortest path from AA to all non-zero valves
# and between all the non-zero valves
steps = dict()
for start in ['AA'] + non_zero:
    steps[start] = bfs(start)

# walk all possible paths between the non-zero valves
# starting from AA with a time limit of 30
def walk(time):
    max_rate = 0
    paths = list()
    to_visit = [('AA', time, 0, set())]
    while to_visit:
        valve, time, rate, visited = to_visit.pop(0)
        #print(valve, time, rate, visited)
        if visited:
            max_rate = max(max_rate, rate)
            paths.append((rate, visited))
        for neighbor in steps[valve]:
            if neighbor in non_zero and neighbor not in visited:
                t = steps[valve][neighbor] + 1
                # can we reach the valve in time?
                if t <= time:
                    tr = time - t
                    r = valves[neighbor].rate * tr
                    r += rate
                    n = (neighbor, tr, r, visited | {neighbor})
                    to_visit.append(n)
    return max_rate, paths

max_rate, paths = walk(30)
print("part1:", max_rate)

# there has to be a better way than testing
# all non-intersecting paths like this, sigh
max_rate, paths = walk(26)
max_rate = 0
for p1 in paths:
    for p2 in paths:
        r1, s1 = p1
        r2, s2 = p2
        #print(s1, s2, r1, r2)
        if not s1 & s2:
            r = r1 + r2
            max_rate = max(max_rate, r)

print("part2:", max_rate)
