# http://gabrielgambetta.com/path6.html

from __future__ import print_function
from math import sqrt

class Node:

    x = None
    y = None
    previous = None
    neighbours = None
    cost = None
    cost_so_far = None

    def __init__(self, x, y, cost=None, previous=None, neighbours=None):
        enforce = [
            [int, False, [x, y]],
            [int, True, [cost]],
            [Node, True, [previous]],
            [list, True, [neighbours]]]

        for e_type, e_nullable, e_params in enforce:
            for e_param in e_params:
                if e_nullable and e_param is None:
                    continue

                if not isinstance(e_param, e_type):
                    raise TypeError("{} not a type {}".format(
                        e_param, e_type))

        self.x = x
        self.y = y

        if cost is not None:
            self.cost = cost

        if previous is not None:
            self.previous = previous

        if neighbours is not None:
            self.neighbours = neighbours
        else:
            self.neighbours = []

        self.cost = 1
        self.cost_so_far = 0

    def __repr__(self):
        return "[{},{}]".format(self.x, self.y)


class Grid:
    width = 0
    height = 0
    data = None

    nodes = []

    reachable = None
    explored = None

    start = None
    goal = None

    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height

        if not isinstance(data, list):
            data = [c for c in data]

        self.set_data(data)

    def reset(self):
        for node in self.nodes:
            node.cost_so_far = 0
            node.previous = None

    def set_data(self, data):
        self.data = data
        self.nodes = [Node(n % self.width, n // self.width) for n in range(len(self.data))]

        node_costs = {' ': 1, '#': 99, 'w': 2}
        potential_reachable = [' ', 'w']

        for i, c in enumerate(self.data):
            cy = i // self.width
            cx = i % self.width

            self.nodes[i].cost = node_costs[c]

            # ignore walls
            if c == '#':
                continue

            # no diagonal movement
            possible = [(0, -1), (-1, 0), (1, 0), (0, 1), ]

            for xo, yo in possible:
                x = cx + xo
                y = cy + yo

                if x < 0 or y < 0:
                    continue

                if x > self.width - 1 or y > self.height - 1:
                    continue
                
                if self.data[y * self.width + x] in potential_reachable:
                    self.nodes[i].neighbours.append(self.nodes[y*self.width + x])


    def set_start(self, x, y):
        self.data[y*self.width + x] = 's'

    def set_end(self, x, y):
        self.data[y*self.width + x] = 'e'

    def __repr__(self):
        rep = ''
        for y in range(self.height):
            rep += '|'

            for x in range(self.width):
                block = self.data[y * self.width + x]
                rep += block

            rep += '|\n'

        return rep

    def estimate_distance(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def estimate_distance_diagonal(self, a, b):
        """same as estimate_distance() but allows for diagonal movement"""
        return math.sqrt( (a.x - b.x)^2 + (a.y - b.y)^2 )


    def choose_node(self):
        best = None
        min_cost = 9999999999 

        reachable = [n for n in self.reachable if n not in self.explored]
        for node in reachable:
            cost_start_to_node = node.cost_so_far
            cost_node_to_goal = self.estimate_distance(node, self.goal)
            total_cost = cost_start_to_node + cost_node_to_goal

            if min_cost > total_cost:
                min_cost = total_cost
                best = node

            #if best is None or best.cost > node.cost:
            #    best = node
        return best
    
    def find_path(self, startcoords, goalcoords):
        start_x, start_y = startcoords
        goal_x, goal_y = goalcoords

        self.start = self.nodes[start_y * self.width + start_x]
        self.goal = self.nodes[goal_y * self.width + goal_x]

        self.reachable = [self.start]
        self.explored = []

        iterations = 0

        while self.reachable:
            # Choose some node we know how to reach
            ne = self.choose_node()

            # If we just got to the goal node build and return the path
            if ne == self.goal:
                path = []

                while ne.previous:
                    path.append(ne)
                    ne = ne.previous

                return path

            # Avoid repeating
            self.reachable.remove(ne)
            self.explored.append(ne)

            # Where can we go from here?
            new_reachable = [n for n in ne.neighbours if n not in self.explored]
            for an in new_reachable:
                if an not in self.reachable:
                    self.reachable.append(an)

                if ne.cost_so_far + an.cost < an.cost_so_far or an.cost_so_far == 0:
                    if an.previous:
                        #print('switching {} to another previous.. {} -> {}'.format(
                        #    an, an.previous, ne))
                        pass

                    an.previous = ne
                    an.cost_so_far = ne.cost_so_far + an.cost

            iterations += 1

        # If we get here, no path was found.
        return None


if __name__ == '__main__':
    """
    
    g = Grid(10, 10,
        '          '
        '          '
        '          '
        '          '
        '          '
        '          '
        '     s  # '
        '       ## '
        '      ##e '
        '       w  ')

    g.find_path()
    print(g)
    """
