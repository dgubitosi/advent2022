
filename = "test.txt"
with open(filename) as f:
    doc = [(i, int(v.strip())) for i, v in enumerate(f.readlines())]
#print([i[-1] for i in doc])

size = len(doc)
current = 0
while current < size:
    for i in range(size):
        if doc[i][0] == current:
            item = doc.pop(i)
            target = item[1] + i
            if target <= 0:
                while target <= 0:
                    target += size
                target -= 1
            if target >= size:
                target %= size
                target += 1
            #print(f'{current}:{i}:{item} shift to {item[1]} => {item[1]+i} => {target}')
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

print(doc[_1000][1] + doc[_2000][1] + doc[_3000][1])
