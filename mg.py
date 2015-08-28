from queue import PriorityQueue, Empty
from random import random, randrange
import math

# inspiration: https://crawl.develz.org/tavern/viewtopic.php?f=9&t=6594&p=88199

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Room:
    width = None
    height = None
    x = None
    y = None
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self):
        ret = []
        for y in range(self.height):
            if y in [0, self.height -1]:
                ret.append('#' * self.width)
            else:
                ret.append('#{}#'.format('.' * (self.width-2)))
        return ret
       

class Gen:
    width = None
    height = None
    data = None

    rooms = []

    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.data = [' ' for x in range(self.width * self.height)]

        # initialize data grid
        for i in range(self.width * self.height):
            self.data[i] = " "

    def c2i(self, x, y):
        return y*self.width + x

    def set(self, x, y, c):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return

        self.data[self.c2i(x, y)] = c

    def get(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return

        return self.data[self.c2i(x, y)]

    def get_next(self, x, y, direction):
        nx, ny = 0, 0
        if direction == UP:
            nx, ny = x, y-1
        elif direction == DOWN:
            nx, ny = x, y+1
        elif direction == LEFT:
            nx, ny = x-1, y
        elif direction == RIGHT:
            nx, ny = x+1, y

        if nx < 0 or nx > self.width - 1 or ny < 0 or ny > self.height - 1:
            raise IndexError()
        
        return nx, ny

    def turn(self, direction, bearing):
        if direction == UP and bearing == LEFT:
            return LEFT
        elif direction == UP and bearing == RIGHT:
            return RIGHT
        elif direction == DOWN and bearing == RIGHT:
            return LEFT
        elif direction == DOWN and bearing == LEFT:
            return RIGHT
        elif direction == LEFT and bearing == RIGHT:
            return UP
        elif direction == LEFT and bearing == LEFT:
            return DOWN
        elif direction == RIGHT and bearing == RIGHT:
            return DOWN
        elif direction == RIGHT and bearing == LEFT:
            return UP
        return

    def add_room(self, x, y, width, height):
        self.rooms.append(Room(x, y, width, height))

    def create_rooms(self):
        rooms = randrange(3, 6)
        for room in range(rooms):
            x, y = math.floor(random() * self.width), math.floor(random() * self.height)
            print('room {}: {},{}'.format(room, x,y))

            width = randrange(3, 25)
            height = randrange(3, 15)

            lf = x - (width // 2)
            tp = y - (height // 2)

            for wx in range(width):
                for wy in range(height):
                    cx = lf + wx
                    cy = tp + wy

                    is_wall = wx in [0, width-1] or wy in [0, height-1]
                    cur = self.get(cx, cy)

                    if is_wall:
                        if cur == '#':
                            self.set(cx, cy, '.')
                        else:
                            self.set(cx, cy, '#')
                    else:
                        self.set(cx, cy, '.')

            self.set(x, y, 'R')

    def generate(self):

        midx = self.width//2
        midy = self.height//2

        self.set(midx, midy, 'X')

        self.explorable = PriorityQueue()
        self.explorable.put((0, (midx-1, midy, LEFT)))
        self.explorable.put((0, (midx+1, midy, RIGHT)))

        c = {0:0, 1:1, 2:2, 3:3}

        try:
            while True:
                priority, (x, y, direction) = self.explorable.get(False)
                self.data[self.c2i(x, y)] = 'x'

                try:
                    nx, ny = self.get_next(x, y, direction)
                    #if self.get(nx, ny) == ' ':
                    #    self.explorable.put((priority, (nx, ny, direction)))

                    TRESHOLD_DOORWAY = 0.01
                    TRESHOLD_TUNNEL = 0.2

                    if priority == 0:
                        # give equal chances of branching left and right
                        if random() >= 1 - TRESHOLD_TUNNEL:
                            # branch right
                            nd = self.turn(direction, RIGHT)
                            nx, ny = self.get_next(nx, ny, nd)
                            self.explorable.put((priority + 0.05, (nx, ny, nd)))
                            
                            c[nd] += 1
                        
                        if random() >= 1 - TRESHOLD_TUNNEL:
                            # branch left
                            nd = self.turn(direction, LEFT)
                            nx, ny = self.get_next(nx, ny, nd)
                            self.explorable.put((priority + 0.05, (nx, ny, nd)))

                            c[nd] += 1

                except IndexError:
                    pass

        except Empty:
            pass

        print(c)

    def embed(self, graphic, target, tw, th):
        xo = graphic.x - graphic.width // 2
        yo = graphic.y - graphic.height // 2

        for y, line in enumerate(graphic.render()):
            for x in range(len(line)):
                cx, cy = x + xo, y + yo
                
                if cx < 0 or cx > tw -1 or cy < 0 or cy > th -1:
                    continue

                ti = cy * tw + cx
                if target[ti] in [' ', '#']:
                    target[ti] = line[x] 
                elif target[ti] == '#' and line[x] == '#':
                    target[ti] = '.'

        return target


    def __repr__(self):
        display = [c for c in self.data]

        for room in self.rooms:
            display = self.embed(room, display, self.width, self.height)

        ret = ''
        for y in range(self.height):
            ret += "{}\n".format(
                    "".join(display[self.c2i(0, y):self.c2i(self.width, y)]))

        return ret


if __name__ == '__main__':
    g = Gen(75, 40)

    for i in range(randrange(10,20)):
        x = randrange(0, 74)
        y = randrange(0, 39)
        w = randrange(5, 15)
        h = randrange(5, 10)

        g.add_room(x, y, w, h)

    # g.generate()
    print(g)
