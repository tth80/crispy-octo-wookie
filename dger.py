from dlib import Grid, Node
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

    def render(self):
        # print("\033[{};{}H".format(self.x+1, self.y+1))
        print(self.x, self.y, end=' ')
        print("E")
        
    def tick(self):
        pass


class EntityRoaming(Entity):
    waypoints = None
    active_waypoint = 0

    grid_ref = None

    def __init__(self):
        super(EntityRoaming, self).__init__()

        self.waypoints = []
        self.active_waypoint = None

    def set_waypoints(self, waypoints):
        self.waypoints = waypoints
        self.active_waypoint = 0

    def set_grid(self, grid):
        self.grid_ref = grid

    def __repr__(self):
        return 'RoamingEntity({},{})'.format(self.x, self.y)
        #return 'Roaming Entity: Heading towards: {} with waypoints {}'.format(
        #    self.waypoints[self.active_waypoint],
        #    self.waypoints)

    def tick(self):
        # remove existing paths
        self.grid_ref.reset()

        active_waypoint = self.waypoints[self.active_waypoint]
        waypoint_count = len(self.waypoints)
        
        cur_loc = [self.x, self.y]
        if cur_loc == active_waypoint:
            #print('{} reached waypoint {}.'.format(self, active_waypoint))

            self.active_waypoint = (self.active_waypoint + 1) % waypoint_count
            active_waypoint = self.waypoints[self.active_waypoint]
            #print('{} new waypoint: {}'.format(self, active_waypoint))

        #print('Search: {} to {}'.format(cur_loc, active_waypoint))
        path = self.grid_ref.find_path(cur_loc, active_waypoint)
        #print(path)
        #oldx, oldy = self.x, self.y
        self.x, self.y = path[-1].x, path[-1].y
        print(self.x, self.y)

        #print("{} moving from {} to {}".format(self, (oldx, oldy), (self.x, self.y)))



class Enemy(EntityRoaming):
    def __repr__(self):
        return super(Enemy, self).__repr__().replace('Entity', 'Enemy')
        

class Game:
    grid = None
    entities = None

    _tick = 0

    def tick(self):
        self._tick += 1
        
        # move all entities
        for entity in self.entities:
            entity.tick()

        # move player
        # calculate damage
        # save the world

    def load_level(self, data):
        self.entities = []

        rows = data.rstrip().split('\n')
        width, height = [int(n) for n in rows[0].split(',')]
        mapdata = ''.join(rows[1:height+1])

        # initialize map grid
        self.grid = Grid(width, height, mapdata)

        # initialize entities
        for entitydata in rows[height+1:]:
            e_type, waypoints = entitydata.split(' ', 1)
            waypoints = [list(map(int, wp.split(','))) for wp in waypoints.split(' ')]

            if e_type == 'E':
                entity = Enemy()
                entity.set_location(*waypoints[0])
                entity.set_waypoints(waypoints)
                entity.set_grid(self.grid)

                self.entities.append(entity)

        # print(':{}:{}:{}:{}:{}:'.format(width, height, width*height, mapdata, len(mapdata)))

    def render(self):
        print("\033[1;1H")

        grid_data = [list(line) for line in str(self.grid).split('\n')]
        for e in self.entities:
            grid_data[e.y][e.x+1] = 'E'

        print('\n'.join([''.join(line) for line in grid_data]))

        #for e in self.entities:
        #    e.render()

        #print("\033[{};1H".format(self.grid.height))
        #print('Entities:')
        #for e in self.entities:
        #    print(e)

        time.sleep(0.01)


if __name__ == '__main__':
    game = Game()

    with open('leveltest.txt') as f:
        data = f.read()
        game.load_level(data)

    for i in range(1000):
        game.tick()
        game.render()
