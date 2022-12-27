
class Valve(object):
    def __init__(self, name, rate=0, neighbors=list()):
        self.name = name
        self.rate = rate
        self.neighbors = neighbors

valves = dict()
non_zero = list()
with open('test.txt') as f:
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

def dijkstra(start, end, visited=None, distances=None, predecessors=None):
    if visited is None: visited = set()
    if distances is None: distances = dict()
    if predecessors is None: predecessors = dict()

    _inf = float('inf')

    if start == end:
        path = []
        while end != None:
            path.append(end)
            end = predecessors.get(end, None)
        return distances[start], path[::-1]

    if not visited:
        distances[start] = 0

    for neighbor in valves[start].neighbors:
        if neighbor not in visited:
            d = distances[start] + 1
            if d < distances.get(neighbor, _inf):
                distances[neighbor] = d
                predecessors[neighbor] = start
    visited.add(start)

    remaining = dict((k, distances.get(k, _inf)) for k in valves if k not in visited)
    nearest = min(remaining, key=remaining.get)

    return dijkstra(nearest, end, visited, distances, predecessors)

# we only care about the non-zero valves
# find shortest path from AA to all non-zero valves
# and between all the non-zero valves
steps = dict()
for start in ['AA'] + non_zero:
    for end in non_zero:
        if start == end: continue
        d, path = dijkstra(start, end)
        steps.setdefault(start, dict()).update({end: d})
        steps.setdefault(end, dict()).update({start: d})

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
            if neighbor not in visited:
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
