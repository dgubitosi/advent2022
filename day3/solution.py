
priority = 0
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        half = len(line)//2
        a = line[:half]
        b = line[half:]
        z = set(a).intersection(set(b))
        output = ""
        for item in z:
            p = ord(item) + 1
            if p >= ord('a'):
                p -= ord('a')
            else:
                p -= ord('A')
                p += 26
            output += f'({item},{p}) '
            priority += p
        print(line, half)
        print(z, a, b)
        print(output)
        print()

print(priority)