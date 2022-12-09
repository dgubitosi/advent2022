from math import dist

h_pos = (0, 0)
t_pos = (0 ,0)
t_visited = set()
t_visited.add(t_pos)

diagonal = dist((0,0), (1,1))

with open('input.txt') as f:
    for line in f:
        direction, steps = line.strip().split(' ', 2)
        move = 0
        for i in range(int(steps)):
            move += 1
            h_start = h_pos
            t_start = t_pos

            hx, hy = h_start
            if direction == 'R':
                hx += 1
            elif direction == 'L':
                hx -= 1
            elif direction == 'U':
                hy += 1
            elif direction == 'D':
                hy -= 1
            h_pos = (hx, hy)

            tx, ty = t_start
            distance = dist(h_pos, t_pos)
            if distance > diagonal:
                if hy > ty:
                    ty += 1
                elif hy < ty:
                    ty -= 1
                if hx > tx:
                    tx += 1
                elif hx < tx:
                    tx -= 1
            t_pos = (tx, ty)
            t_visited.add(t_pos)

            print(f'[{direction} {steps}] {move} head={h_start}->{h_pos} tail={t_start}->{t_pos}')

print(t_visited)
print(len(t_visited))