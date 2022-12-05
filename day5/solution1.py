
def build_stacks(stack_input):
    #print("\n".join(stack_input))
    stacks = {}
    positions = [int(pos) for pos, stack in enumerate(stack_input[-1]) if stack.isnumeric()]
    #print(positions)
    i = len(stack_input) - 2
    while i >= 0:
        for stack, pos in enumerate(positions):
            try:
                c = stack_input[i][pos]
                if c.isalpha():
                    stacks.setdefault(stack+1, []).append(c)
            except:
                pass
        i -= 1
    #print(stacks)
    return stacks

with open('input.txt') as f:
    stack_input = []
    stacks = None
    for line in f:
        line = line.rstrip()
        if line.startswith('move'):
            count, source, dest = [int(word) for pos, word in enumerate(line.split(' ')) if pos % 2 == 1]
            #print(source, count, dest)
            s = stacks[source][-count::]
            stacks[source] = stacks[source][:-count]
            stacks[dest] += s[::-1]
            #print(stacks)
        elif not line and stacks is None:
            stacks = build_stacks(stack_input)
        else:
            stack_input.append(line)

    message = ''
    for s in sorted(stacks):
        message += stacks[s][-1]
    print(message)
