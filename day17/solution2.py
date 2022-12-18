
class Shapes():
    def __init__(self):
        self.shapes = [
            # bottom is index 0
            [[1,1,1,1]],
            [[0,1,0],[1,1,1],[0,1,0]],
            [[1,1,1],[0,0,1],[0,0,1]],
            [[1],[1],[1],[1]],
            [[1,1],[1,1]],
        ]
        # no shape to start
        self.active = -1

    def next(self):
        self.active += 1
        if self.active == len(self.shapes):
            self.active = 0
        #return self.shapes[self.active]

    def current(self):
        if self.active >= 0 and self.active < len(self.shapes):
            return self.shapes[self.active]
        return None

    @property
    def height(self):
        if self.active >= 0 and self.active < len(self.shapes):
            return len(self.shapes[self.active])
        return 0

    @property
    def width(self):
        if self.active >= 0 and self.active < len(self.shapes):
            return len(self.shapes[self.active][0])
        return 0


class Game():
    def __init__(self, _print=False, _debug=False):
        self._print = _print
        self._debug = _debug

        # shapes
        self.shapes = Shapes()
        self.shape = None
        self.corner = None # (y, x) lower left corner

        # initial board
        self.field = list()
        self.placed = 0
        self.tower = 0
        self.width = 7
        self.truncated = 0

        # initial shape
        self.next_shape()

    @property
    def height(self):
        # height of the play field
        return len(self.field)

    @property
    def edges(self):
        # edges of the current shape
        bottom = self.corner[0]
        top = bottom + self.shapes.height - 1
        left = self.corner[1]
        right = left + self.shapes.width - 1
        return (top, bottom, left, right)

    def next_shape(self):
        # places the next shape on the field
        self.shapes.next()
        self.shape = self.shapes.current()

        # clear the top of the field
        y = self.height - 1
        while y >= 0:
            result = sum(self.field[y])
            if result:
                break
            del self.field[y]
            y -= 1

        # update tower height
        self.tower = self.truncated + y + 1

        # extend field by 3 rows
        h = self.height + 3
        for y in range(self.height, h):
            self.field.append([0]*self.width)

        # place the new shape above
        # extend the field by the height of the new shape
        self.corner = (self.height, 2)
        for y in range(h, h + self.shapes.height):
            self.field.append([0]*self.width)
        self.draw_shape(1)

        if self.height % 100 == 0:
            self.truncate()

        if self._print:
            print('placed:', self.placed)
            print('height:', self.tower)
            self.print()
            print()

    def truncate(self):
        #print("truncating field", self.height)
        y = self.height - 1
        chunk = 3
        while y >= chunk:
            bottom = y - chunk
            columns = 0
            #print(y, bottom)
            for x in range(self.width):
                result = sum([self.field[y][x] for y in range(y, bottom, -1)])
                #print(x, result)
                if result:
                    columns += 1
            #print(columns)
            if columns == self.width:
                #print('** TRUNCATED **')
                # we can remove below the chunk
                self.truncated += bottom
                self.field = self.field[bottom:]
                self.corner = (self.corner[0] - bottom, self.corner[1])
                break
            y -= 1

    def move(self, direction):
        # move left or right
        self.left_right(direction)

        # move down
        # returns if the block is at rest
        _at_rest = self.down()
        if _at_rest:
            self.placed += 1
            self.draw_shape(2)
            self.next_shape()

    def left_right(self, direction):
        # try to move left or right
        _x = 1
        if direction == '<':
            _x = -1

        # edges
        top, bottom, left, right = self.edges

        _left = left + _x
        _right = right + _x

        can_move = False
        if self._debug: print(direction, self.corner, self.shapes.active, self.shape)
        if _left >= 0 and _right < self.width:
            if _x > 0:
                # check right edge
                result = [self.field[y][right] + self.field[y][_right] for y in range(bottom, top+1)]
            else:
                # check left edge
                result = [self.field[y][left] + self.field[y][_left] for y in range(bottom, top+1)]

            if self._debug: print('lr', result)
            if max(result) <= 2:
                can_move = True

            # extra check for the cross
            if self.shapes.active == 1 and can_move:
                if _x > 0:
                    # check right edge
                    result = [self.field[y][right-1] + self.field[y][_right-1] for y in range(bottom, top+1)]
                else:
                    # check left edge
                    result = [self.field[y][left+1] + self.field[y][_left+1] for y in range(bottom, top+1)]

                if self._debug: print('lr', result)
                if max(result) > 2:
                    can_move = False

        if can_move:
            self.draw_shape(0)
            self.corner = (bottom, _left)
            self.draw_shape(1)
            if self._debug: print('moved', direction, self.corner)

    def down(self):
        # try to move down
        _at_rest = False
        
        # edges
        top, bottom, left, right = self.edges

        if bottom == 0:
            _at_rest = True
        else:
            # check the bottom row
            slice0 = self.field[bottom][left:right+1]
            slice1 = self.field[bottom-1][left:right+1]
            result = [sum(i) for i in zip(slice0, slice1)]
            if self._debug: print('dn', result)
            if max(result) > 2:
                _at_rest = True

            # extra check for the cross
            if self.shapes.active == 1 and not _at_rest:
                slice0 = self.field[bottom+1][left:right+1]
                slice1 = self.field[bottom][left:right+1]
                result = [sum(i) for i in zip(slice0, slice1)]
                if self._debug: print('dn', result)
                if max(result) > 2:
                    _at_rest = True

            if not _at_rest:
                self.draw_shape(0)
                self.corner = (bottom-1, left)
                self.draw_shape(1)
                if self._debug: print('moved', '-', self.corner)

        return _at_rest

    def draw_shape(self, value=1):
        # value 0 = erase
        # value 1 = falling
        # value 2 = at rest

        top, bottom, left, right = self.edges
        _y = (bottom, top+1)
        _x = (left, right+1)

        for y in range(*_y):
            for x in range(*_x):
                if self.shape[y-bottom][x-left]:
                    self.field[y][x] = value

        if self._print:
            self.print()
            print()

    def print(self):
        icons = ['.', '@', '#']
        y = self.height - 1
        while y >= 0:
            row = '|'
            for x in range(self.width):
                #row += str(self.field[y][x])
                row += icons[self.field[y][x]]
            row += f'| {self.truncated+y+1}'
            print(row)
            y -= 1
        print('+-------+', self.truncated)


with open('input.txt') as f:
    jets = list(f.readline().strip())

import sys
count = 1_000_000_000_000
if len(sys.argv) > 1:
    try:
        count = int(sys.argv[1])
    except:
        pass

import time
st = time.time()
game = Game() #_print=True, _debug=True)
while True:
    if game.placed % 1000 == 0:
        et = time.time()
        print(f'{game.placed} .. {et:.3f}')

    for j in jets:
        game.move(j)

        if game.placed == count:
            break

    if game.placed == count:
        break

game.print()
print('tower height:', game.tower)
