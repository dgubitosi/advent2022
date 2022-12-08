
files = {}
directories = {}

with open('input.txt') as f:
    path = []
    command = ""
    for line in f:
        line = line.strip()
        if not line:
            continue
        line = line.split(' ')
        if line[0] == '$':
            command = ' '.join(line[1:])
            if line[1] == 'cd':
                target = line[-1]
                if target == '..':
                    path = path[:-1]
                else:
                    if target == '/':
                        target = ''
                    path.append(target)
                p = '/'.join(path) + '/'
                print(f'{command} -> cd {p}')
            elif line[1] == 'ls':
            
                p = '/'.join(path) + '/'
                directories.setdefault(p, 0)
                print(f'{command}')
        elif command == 'ls':
            size, name = line[0], line[1]
            is_file = size.isnumeric()
            is_dir = not is_file
            p = '/'.join(path) + '/'
            name = p + name
            print(f'{name}, {size}')
            if is_dir:
                directories.setdefault(p, 0)
            if is_file:
                # file
                size = int(size)
                files[name] = size
                for i in range(len(path)):
                    p = '/'.join(path[:i+1]) + '/'
                    directories[p] += size

under_100_000 = 0
for d in directories:
    flag = ""
    if directories[d] <= 100_000:
        flag += "*"
        under_100_000 += directories[d]
    print(d, directories[d], flag)
print(under_100_000)

total = 70_000_000
minimum = 30_000_000
used = directories['/']
available = total - used
needed = minimum - available

print()
print(needed)

candidates = {}
for d in directories:
    size = directories[d]
    if size >= needed:
        candidates.setdefault(size, []).append(d)

print(sorted(candidates)[0])
for c in sorted(candidates):
    print(c, candidates[c])
