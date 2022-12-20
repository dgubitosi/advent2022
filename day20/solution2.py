
filename = "input.txt"
with open(filename) as f:
    # add decryption key
    doc = [(i, int(v.strip())*811589153) for i, v in enumerate(f.readlines())]
#print([i[-1] for i in doc])
size = len(doc)
last = size - 1

# repeat 10 times
for count in range(10):
    current = 0
    while current < size:
        for i in range(size):
            if doc[i][0] == current:
                item = doc.pop(i)
                target = item[1] + i
                target %= last
                doc.insert(target, item)
                break
        #print([i[-1] for i in doc])
        current += 1

#print([i[-1] for i in doc])

# find zero
zero = None
for i in range(size):
    if doc[i][1] == 0:
        zero = i
        break

_1000 = (zero + 1000) % size
_2000 = (zero + 2000) % size
_3000 = (zero + 3000) % size

print("part2:", doc[_1000][1] + doc[_2000][1] + doc[_3000][1])
