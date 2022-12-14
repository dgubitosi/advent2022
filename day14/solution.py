
ROCK = '#'
SAND = 'o'

x_range = [None, 0]
y_range = [None, 0]

board = dict()

class Board:
    def __init__(self):
        self.positions = dict()
        self.x_lo = 0
        self.x_hi = 0
        self.y_lo = 0
        self.y_hi = 0

    def add(self, position, item):
        self.positions[position] = item
        x, y = position
        #print("add", x, y, item)

        if self.x_lo == 0:
            self.x_lo = x
        else:
            self.x_lo = min(self.x_lo, x)
        self.x_hi = max(self.x_hi, x)
        self.y_hi = max(self.y_hi, y)

    def get(self, position):
        #print("get", position)
        if position not in self.positions:
            if position[1] > self.y_hi:
                raise Exception('Void!')
            self.add(position, False)
        #print("return", self.positions[position])
        return self.positions[position]

    def drop(self, position):
        self.drop = position
        self.add(self.drop, '+')

    def fall(self):
        count = 0
        try:
            while True:
                count += 1

                # start at 500, 0 and drop until something
                # is hit
                x, y = self.drop
                y += 1
                while True:
                    # keep dropping
                    while not self.get((x, y)):
                        y += 1

                    under = board.get((x, y))
                    # sand encountered something
                        # try to move left or right
                    if under:
                        # diagonal left
                        if not self.get((x-1, y)):
                            x -= 1
                        # diagonal right
                        elif not self.get((x+1, y)):
                            x += 1
                        # stuck
                        else:
                            y -= 1
                            break

                self.add((x, y), SAND)
                #print(count, (x,y))
                #self.print()
        except:
            pass

        self.rest = count - 1
        return self.rest

    def print(self):
        #print("y:", self.y_lo, "-", self.y_hi)
        #print("x:", self.x_lo, "-", self.x_hi)
        for y in range(self.y_lo, self.y_hi+1):
            row = ''
            for x in range(self.x_lo, self.x_hi+1):
                item = self.get((x,y))
                if item:
                    row += item
                else:
                    row += '.'
            print(row)

board = Board()
with open('input.txt') as f:
    for line in f:
        line = line.strip().split(' -> ')
        #print(line)
        pos = list()
        for item in line:
            x, y = item.split(',', 2)
            p = (int(x), int(y))
            pos.append(p)
        for i in range(1, len(pos)):
            start = pos[i-1]
            end = pos[i]
            min_x = min(start[0], end[0])
            max_x = max(start[0], end[0])+1
            min_y = min(start[1], end[1])
            max_y = max(start[1], end[1])+1
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    board.add((x, y), ROCK)

# drop point
board.drop((500, 0))

# part 1
print(board.fall())
