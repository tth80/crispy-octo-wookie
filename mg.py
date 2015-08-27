from queue import PriorityQueue, Empty
from random import random

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Gen:
    width = None
    height = None
    data = None

    def c2i(self, x, y):
        return y*self.width + x

    def set(self, x, y, c):
        self.data[self.c2i(x, y)] = c

    def get(self, x, y):
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

    def generate(self):
        self.width = 75
        self.height = 40

        self.data = [' ' for x in range(self.width * self.height)]

        # initialize data grid
        for i in range(self.width * self.height):
            self.data[i] = "."

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
                    if self.get(nx, ny) == '.':
                        self.explorable.put((priority, (nx, ny, direction)))

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


    def __repr__(self):
        ret = ''
        for y in range(self.height):
            ret += "{}\n".format(
                    "".join(self.data[self.c2i(0, y):self.c2i(self.width, y)]))

        return ret


if __name__ == '__main__':
    g = Gen()
    g.generate()
    print(g)
