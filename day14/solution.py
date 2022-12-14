
class IntoTheVoid(Exception):
    "Raised when no more sand is at rest"
    pass

class Board:

    def __init__(self, drop=None, print=False, debug=False):
        if drop: self.drop = drop

        self._print = print
        self._debug = debug

        self.positions = dict()
        self.x_lo = 0
        self.x_hi = 0
        self.y_lo = 0
        self.y_hi = 0
        self.at_rest = 0
        self.floor = False

    def debug(self, debug=False):
        self._debug = debug

    def rock(self, position):
        self.add(position, '#')

    def sand(self, position):
        self.add(position, 'o')

    def air(self, position):
        self.add(position, False)

    def add(self, position, item):
        self.positions[position] = item
        x, y = position
        if self._debug: print("add", x, y, item)

        if self.x_lo == 0:
            self.x_lo = x
        else:
            self.x_lo = min(self.x_lo, x)
        self.x_hi = max(self.x_hi, x)
        self.y_hi = max(self.y_hi, y)

    def get(self, position):
        if self._debug: print("get", position)
        if position not in self.positions:
            x, y = position
            # part1 does not have a floor
            if not self.floor:
                # we're past the bottom!
                if y > self.y_hi:
                    raise IntoTheVoid
                else:
                    self.air(position)
            # part2 adds a floor
            else:
                # builds the floor
                if y == self.floor + 1:
                    if self._debug: print("setting floor at", position)
                    self.air(position)
                    self.rock((x, y + 1))
                # builds the floor
                elif y == self.floor + 2:
                    if self._debug: print("setting floor at", position)
                    self.rock(position)
                else:
                    self.air(position)

        if self._debug: print("return", self.positions[position])
        return self.positions[position]

    def add_floor(self, floor=True):
        if floor:
            self.floor = self.y_hi
        else:
            self.floor = False

    def drop(self, position):
        self.drop = position

    def fall(self):
        count = self.at_rest
        try:
            while True:
                count += 1

                if not self.get(self.drop):
                    x, y = self.drop
                # drop position is occupied!
                else:
                    break

                while True:
                    # keep dropping
                    while not self.get((x, y)):
                        y += 1

                    under = self.get((x, y))
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

                self.sand((x, y))
                if self._debug: print("count", count, (x,y))
                if self._print: self.print()

        # done
        except IntoTheVoid:
            pass

        self.at_rest = count - 1
        return self.at_rest

    def print(self):
        if self._debug:
            print("y:", self.y_lo, "-", self.y_hi)
            print("x:", self.x_lo, "-", self.x_hi)
        for y in range(self.y_lo, self.y_hi+1):
            row = ''
            for x in range(self.x_lo, self.x_hi+1):
                item = self.get((x,y))
                if item:
                    row += item
                else:
                    row += '.'
            print(row)

board = Board(drop=(500,0))
with open('input.txt') as f:
    for line in f:
        line = line.strip().split(' -> ')
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
                    board.rock((x, y))

# part 1
print("part1")
at_rest = board.fall()
print(at_rest)

# part 2
print()
print("part2")
board.add_floor()
at_rest = board.fall()
print(at_rest)
