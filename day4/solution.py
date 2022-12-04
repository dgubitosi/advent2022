
contains = 0
overlaps = 0
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        a, b = line.split(',')
        a = sorted([int(i) for i in a.split('-')])
        b = sorted([int(i) for i in b.split('-')])
        print(a, b)
        # a contains b
        if b[0] >= a[0] and b[1] <= a[1]:
            print(a, 'contains', b)
            contains += 1 
        # b contains a
        elif a[0] >= b[0] and a[1] <= b[1]:
            print(b, 'contains', a)
            contains += 1
        # overlaps
        if a[0] <= b[0] <= a[1]:
            print(f'{a[0]} <= {b[0]} <= {a[1]}')
            overlaps += 1
        elif a[0] <= b[1] <= a[1]:
            print(f'{a[0]} <= {b[1]} <= {a[1]}')
            overlaps += 1
        elif b[0] <= a[0] <= b[1]:
            print(f'{b[0]} <= {a[0]} <= {b[1]}')
            overlaps += 1
        elif b[0] <= a[1] <= b[1]:
            print(f'{b[0]} <= {a[1]} <= {b[1]}')
            overlaps += 1
        print()
print('contains', contains)
print('overlaps', overlaps)