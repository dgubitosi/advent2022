filename = "test.txt"

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

        # backup so we reset
        self._backup = [ self.value, self.op, self.a, self.b ]

    def reset(self):
        self.value, self.op, self.a, self.b = self._backup

monkeys = dict()
to_solve = list()
with open(filename) as f:
    for line in f:
        array = line.strip().split()
        name = array[0][:-1]
        if name == 'humn':
            m = Monkey(name)
            monkeys[name] = m
        if name == 'root':
            array[2] = '='
        if len(array) == 2:
            val = array[1]
            m = Monkey(name, val)
        else:
            op = array[2]
            a = array[1]
            b = array[3]
            m = Monkey(name, op, a, b)
            # better to pre-compute
            to_solve.append(name)
        monkeys[name] = m

def solve(monkeys, to_solve):
    to_solve_now = to_solve[:]
    while to_solve_now:
        name = to_solve_now.pop(0)
        #print(name)
        m = monkeys[name]
        if m.value is None:
            a = monkeys[m.a].value
            b = monkeys[m.b].value
            if a is not None and b is not None:
                if name == 'root':
                    return a, b
                if m.op == '+': m.value = a + b
                elif m.op == '-': m.value = a - b
                elif m.op == '*': m.value = a * b
                elif m.op == '/': m.value = a / b
            else:
                to_solve_now.append(name)
    return None, None

for n in range(1_000_000):
    # reset the monkeys
    for m in monkeys:
        monkeys[m].reset()
    monkeys['humn'].value = n
    
    a, b = solve(monkeys, to_solve)
    print(n, int(abs(a - b)), a, b)
    if a == b:
        print("part2:", n)
        break
