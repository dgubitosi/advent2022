import pprint

elves = dict()
i = 1
elf = 0
max_calories = 0
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        if not line:
            i += 1
        else:
            calories = int(line)
            elves.setdefault(i, 0)
            total = elves[i] + calories
            elves[i] = total

            # track max while reading input
            if total > max_calories:
                elf = i
                max_calories = total

# max
print(elf, max_calories)

top_three = 0
for i, e in enumerate(sorted(elves.items(), key=lambda item: item[1], reverse=True)):
    if i == 3:
        break
    print(e)
    top_three += e[1]
print(top_three)
