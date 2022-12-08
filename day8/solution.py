
grid = []
with open('input.txt') as f:
    for line in f:
        grid.append([int(i) for i in line.strip()])

# rectangular grid
height = len(grid)
width = len(grid[0])

# edges
top_edge = 0
bottom_edge = height-1
left_edge = 0
right_edge = width-1

# set of all visible positions as tuples
visible = set()

# scenic score
scenic_score = 0

for i in range(height):
    row = grid[i]
    for j in range(width):
        column = [grid[row_i][j] for row_i in range(height)]

        # current tree
        tree = grid[i][j]

        #print(i, j, tree)
        #print(row)
        #print(column)

        # edges
        if i in [top_edge, bottom_edge] or j in [left_edge, right_edge]:
            visible.add((i, j))

        # interior
        else:
            # view in each direction
            up = column[:i]
            down = column[i+1:]
            left = row[:j]
            right = row[j+1:]

            # visibility
            if tree > max(up):
                visible.add((i, j))
            if tree > max(down):
                visible.add((i, j))

            if tree > max(left):
                visible.add((i, j))
            if tree > max(right):
                visible.add((i, j))

            # score
            scores = [0]*4
            for t in reversed(up):
                if t <= tree:
                    scores[0] += 1
                if t >= tree:
                    break
            for t in down:
                if t <= tree:
                    scores[1] += 1
                if t >= tree:
                    break
            for t in reversed(left):
                if t <= tree:
                    scores[2] += 1
                if t >= tree:
                    break
            for t in right:
                if t <= tree:
                    scores[3] += 1
                if t >= tree:
                    break
            score = scores[0]*scores[1]*scores[2]*scores[3]
            scenic_score = max(scenic_score, score)

print(len(visible))
print(scenic_score)
