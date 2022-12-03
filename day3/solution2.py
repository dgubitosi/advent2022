
priority = 0
with open('input.txt') as f:
    lines = []
    for line in f:
        lines.append(line.strip())
        if len(lines) < 3:
            continue

        z = set.intersection(*[set(l) for l in lines])
        output = ""
        for item in z:
            p = ord(item) + 1
            if p >= ord('a'):
                p -= ord('a')
            else:
                p -= ord('A')
                p += 26
            priority += p
            output += f'({item},{p}) '
        print(output)
        print()

        # reset
        lines = []

print(priority)