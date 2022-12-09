from math import dist

# rope is 10 knots
# head = rope[0]
# tail = rope[-1]
rope = [(0,0) for i in range(10)]
t_visited = set()
t_visited.add(rope[-1])

diagonal = dist((0,0), (1,1))

with open('input.txt') as f:
    for line in f:
        direction, steps = line.strip().split(' ', 2)
        move = 0
        for i in range(int(steps)):
            move += 1

            # move head first
            h_start = rope[0]
            hx, hy = h_start

            if direction == 'R':
                hx += 1
            elif direction == 'L':
                hx -= 1
            elif direction == 'U':
                hy += 1
            elif direction == 'D':
                hy -= 1
            rope[0] = (hx, hy)

            # move subsequent knots relative to the
            # previous knot
            for j in range(1, len(rope)):
                previous = rope[j-1]
                px, py = previous

                knot = rope[j]
                kx, ky = knot

                distance = dist(previous, knot)
                if distance > diagonal:
                    if py > ky:
                        ky += 1
                    elif py < ky:
                        ky -= 1
                    if px > kx:
                        kx += 1
                    elif px < kx:
                        kx -= 1
                rope[j] = (kx, ky)
            t_visited.add(rope[-1])

            print(f'[{direction} {steps}] {move} head={h_start}->{rope[0]} tail={rope[-1]}')

print(t_visited)
print(len(t_visited))