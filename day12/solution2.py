
start = list()
end = None
graph = dict()
with open("input.txt") as f:
    y = 0
    for line in f:
        for x, c in enumerate(list(line.strip())):
            pos = (y, x)
            elevation = ord(c)-ord('a')+1 # a=1, z=26
            if c == 'S':
                elevation = 1
            elif c == 'E':
                end = pos
                elevation = 26
            if elevation == 1:
                start.append(pos)
            graph[pos] = elevation
        y += 1

results = dict()
for s in start:
    # initialize
    to_visit = [(0, s)]
    visited = list()
    parent = dict()
    cost = dict()

    # walk the graph
    while to_visit:
        _cost, node = to_visit.pop(0)
        #print(_cost, node)

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

    if end in cost:
        _cost = cost[end]
        results[s] = _cost
    else:
        _cost = 'inf'
    print("S:", s, "->", "E:", end, "cost:", _cost)


results = sorted(results.items(), key=lambda x: x[1])
print(results[0])
