
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
max_rate = 0
to_visit = [('AA', 30, 0, list())]
while to_visit:
    valve, time, rate, visited = to_visit.pop(0)
    #print(valve, time, rate, visited)
    for neighbor in steps[valve]:
        if neighbor not in visited:
            t = steps[valve][neighbor] + 1
            # can we reach the valve in time?
            if t <= time:
                tr = time - t
                r = valves[neighbor].rate * tr
                r += rate
                max_rate = max(max_rate, r)
                n = (neighbor, tr, r, visited + [neighbor])
                to_visit.append(n)

print("part1:", max_rate)
