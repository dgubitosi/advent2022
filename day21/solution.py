filename = "input.txt"

class Monkey():
    def __init__(self, name, op=None, a=None, b=None):
        self.name = name
        try:
            self.value = int(op)
            self.op = None
        except:
            self.value = None
            self.op = op
        self.a = a
        self.b = b

monkeys = dict()
to_solve = list()
with open(filename) as f:
    for line in f:
        array = line.strip().split()
        name = array[0][:-1]
        if len(array) == 2:
            val = array[1]
            m = Monkey(name, val)
        else:
            op = array[2]
            a = array[1]
            b = array[3]
            m = Monkey(name, op, a, b)
            to_solve.append(name)
        monkeys[name] = m

while to_solve:
    name = to_solve.pop(0)
    print(name)
    m = monkeys[name]
    if m.value is None:
        a = monkeys[m.a].value
        b = monkeys[m.b].value
        if a is not None and b is not None:
            if m.op == '+': m.value = a + b
            elif m.op == '-': m.value = a - b
            elif m.op == '*': m.value = a * b
            elif m.op == '/': m.value = a / b
        else:
            to_solve.append(name)

for n in monkeys:
    print(n, monkeys[n].value)

print("part1:", monkeys['root'].value)
