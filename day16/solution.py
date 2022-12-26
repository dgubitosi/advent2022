
class Valve(object):
    def __init__(self, name, rate=0, state=False, neighbors=[]):
        self.name = name
        self.rate = rate
        self._open = state
        self.neighbors = neighbors

    def open(self):
        self._open = True

    def is_opened(self):
        return self._open

    def is_closed(self):
        return not self._open

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
        valve = Valve(v, r, False, n)
        valves[v] = valve

def dijkstra(graph, start, end, visited=set(), distances=dict(), predecessors=dict()):
    _inf = float('inf')

    if start == end:
        path = []
        while end != None:
            path.append(end)
            end = predecessors.get(end, None)
        return distances[start], path[::-1]

    if not visited:
        distances[start] = 0

    for neighbor in graph[start].neighbors:
        if neighbor not in visited:
            d = distances[start] + 1
            if d < distances.get(neighbor, _inf):
                distances[neighbor] = d
                predecessors[neighbor] = start
    visited.add(start)

    remaining = dict((k, distances.get(k, _inf)) for k in graph if k not in visited)
    nearest = min(remaining, key=remaining.get)

    return dijkstra(graph, nearest ,end, visited, distances, predecessors)

factorial = 1
for i in range(1, len(non_zero)+1):
    factorial *= i
print(f'{len(non_zero)}, {factorial:_}')

# ok so brute force aint gonna work for the real input
exit()

import itertools
permutations = itertools.permutations(non_zero)
r_max = 0
n = 0
for p in permutations:
    t = 0
    i = 1
    rate = 0
    p = list(p)
    p.insert(0, 'AA')
    while i < len(p):
        start = p[i-1]
        end = p[i]
        d, path = dijkstra(valves, start, end, visited=set(), distances=dict(), predecessors=dict())
        t += d + 1
        if t > 30: break
        rate += valves[end].rate * (30-t)
        r_max = max(r_max, rate)
        i += 1
    n += 1
    print(n)

print()
print(r_max)
