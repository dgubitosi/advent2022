

MONKEYS = {}
with open('test.txt') as f:
    monkey = None
    for line in f:
        line = line.strip()
        if not line:
            monkey = None
            continue
        line = line.split()
        if line[0] == 'Monkey':
            m = line[1].split(':')[0]
            monkey = int(m)
            #print(monkey)
            MONKEYS.setdefault(monkey, dict())
            MONKEYS[monkey]['inspections'] = 0
        elif line[0] == 'Starting':
            items = [int(i) for i in ''.join(line[2:]).split(',')]
            #print(monkey, items)
            MONKEYS[monkey]['items'] = items
        elif line[0] == 'Operation:':
            op = line[4:]
            if op[-1] == 'old':
                op = ['sq']
            else:
                op[-1] = int(op[-1])
            #print(monkey, op)
            MONKEYS[monkey]['worry'] = op
        elif line[0] == 'Test:':
            test = int(line[-1])
            #print(monkey, test)
            MONKEYS[monkey]['test'] = test
        elif line[0] == 'If':
            test = line[1] == 'true:'
            n = int(line[-1])
            #print(monkey, test, n)
            MONKEYS[monkey][test] = n

def update_worry(a, op, b=0):
    new = a
    s = ''
    if op == '+':
        s += f'increases by {b}'
        new +=  b
    elif op == '*':
        s += f'mulitiplied by {b}'
        new *= b
    elif op == 'sq':
        s += 'multipied by itself'
        new *= a
    return new, s

import time
st = time.time()

for c in range(100):
    _round = c + 1
    _print = False
    if _round == 1 or _round % 10 == 0: #_round % 1000 == 0:
        _print = True
        et = time.time() - st
        print(f'\n{et}\n== After round {_round} ==')
    for m in MONKEYS:
        monkey = MONKEYS[m]
        items = monkey['items']
        monkey['inspections'] += len(items)
        if _print:
            print(f'Monkey {m} inspected items {monkey["inspections"]} times.')
            print(f'.. {monkey["items"]}')
        while items:
            item = monkey['items'].pop(0)
            #print(f'  Monkey inspects an item with worry level of {item}.')
            worry, s = update_worry(item, *monkey['worry'])
            #print(f'    Worry level is {s} to {worry}')
            #worry = worry // 3
            test = monkey['test']
            #print(f'    Monkey gets bored with item. Worry level is divided by 3 to {worry}.')
            _true = worry % test == 0
            is_not = '' if _true else ' not '
            #print(f'    Current worry level is{is_not}divisible by {test}.')
            next_monkey = monkey[_true]
            #print(f'    Item with worry level {worry} is thrown to monkey {next_monkey}.')
            MONKEYS[next_monkey]['items'].append(worry)

activity = sorted(MONKEYS, key=lambda m: MONKEYS[m]['inspections'], reverse=True)
monkey_business = 1
for i in range(2):
    monkey_business *= MONKEYS[activity[i]]['inspections']
print()
print(monkey_business)
