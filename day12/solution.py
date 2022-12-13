
start = None
end = None
graph = dict()
with open("input.txt") as f:
    y = 0
    for line in f:
        for x, c in enumerate(list(line.strip())):
            elevation = ord(c)-ord('a')+1 # a=1, z=26
            if c == 'S':
                start = (y, x)
                elevation = 1
            elif c == 'E':
                end = (y, x)
                elevation = 26
            graph[(y,x)] = elevation
        y += 1

# initialize
to_visit = [(0, start)]
visited = list()
parent = dict()
cost = dict()

# walk the graph
while to_visit:
    _cost, node = to_visit.pop(0)
    print(_cost, node)

    if node not in visited:
        visited.append(node)
        cost[(node)] = _cost
        if node == end:
            break

        # find valid adjacent neighbors
        for a in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (node[0] + a[0], node[1] + a[1])
            if neighbor in graph and graph[neighbor] <= graph[node] + 1:
                to_visit.append((_cost + 1, neighbor))
        to_visit.sort(key=lambda x: x[0])

print("S:", start, "->", "E:", end)
print(cost[end])

