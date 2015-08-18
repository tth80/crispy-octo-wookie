from grid import Grid, Node
import time
from functools import wraps

def timing(f):
    @wraps(f)
    def with_timing(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()

        ms = (time2-time1)*1000.0
        fps = int(1000/ms)

        print('[{}] function took {:2f} ms. ({:d} fps)'.format(f.__name__, ms, fps))
        return ret

    return with_timing


class Entity:
    x = None
    y = None

    def __init__(self):
        pass

    def set_location(self, x, y):
        self.x = x
        self.y = y


class EntityRoaming(Entity):
    waypoints = None
    active_waypoint = None

    def __init__(self):
        super(EntityRoaming, self).__init__()

        self.waypoints = []
        self.active_waypoint = None

    def set_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.active_waypoint = self.waypoints[0]


class Enemy(EntityRoaming):
    pass

class Game:
    grid = None
    entities = None

    def load_level(self, data):
        self.entities = []

        rows = data.rstrip().split('\n')
        width, height = [int(n) for n in rows[0].split(',')]
        mapdata = ''.join(rows[1:height+1])

        for entitydata in rows[height+1:]:
            e_type, waypoints = entitydata.split(' ', 1)
            waypoints = [wp.split(',') for wp in waypoints.split(' ')]

            if e_type == 'E':
                entity = Enemy()
                entity.set_location(*waypoints[0])
                entity.set_waypoints(waypoints)

                self.entities.append(entity)

        # print(':{}:{}:{}:{}:{}:'.format(width, height, width*height, mapdata, len(mapdata)))
        self.grid = Grid(width, height, mapdata)

    @timing
    def render(self):
        print("\033[1;1H")
        print(self.grid)


if __name__ == '__main__':
    game = Game()

    with open('level1.txt') as f:
        data = f.read()
        game.load_level(data)

    for i in range(10):
        game.render()
