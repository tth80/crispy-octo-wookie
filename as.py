# http://gabrielgambetta.com/path2.html

from __future__ import print_function

class Node:
    index = None
    cost = None
    previous = None
    neighbours = None
    node_cost = 0

    def __init__(self, index, cost=None, previous=None, neighbours=None):
        self.index = index

        if cost is not None:
            self.cost = cost

        if previous is not None:
            self.previous = previous

        if neighbours is not None:
            self.neighbours = neighbours
        else:
            self.neighbours = []

    def __repr__(self):
        return "{}".format(self.index)

    def get_cost(self):
        if self.cost is None:
            return 0
        else:
            return self.cost


class grid:
    width = 0
    height = 0
    data = None

    nodes = []

    def __init__(self, width, height, data=None):
        self.width = width
        self.height = height

        if not isinstance(data, list):
            data = [c for c in data]

        self.set_data(data)

    def set_data(self, data):
        self.data = data
        self.nodes = [Node(index=n) for n in range(len(self.data))]

        node_costs = {' ': 1, '#': 99, 'w': 2}

        for i, c in enumerate(self.data):
            cy = i / self.width
            cx = i % self.width

            if c in ['s', 'e']:
                c = ' '

            self.nodes[i].node_cost = node_costs[c]

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

                if self.data[y * self.width + x] == ' ':
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

    def find_path(self):
        def choose_node(reachable, explored):
            lst = [n for n in reachable if n not in explored]
            best = None
            for node in lst:
                if best is None or best.cost > node.cost:
                    best = node
            return best

        start = self.nodes[self.data.index('s')]
        goal = self.nodes[self.data.index('e')]

        reachable = [start]
        explored = []
        previous = {}
        cost = {}

        iterations = 0

        while reachable:
            # Choose some node we know how to reach
            ne = choose_node(reachable, explored)

            # If we just got to the goal node build and return the path
            if ne == goal:
                path = []

                while ne != None:
                    path.append(ne)
                    ne = ne.previous

                for n in path:
                    self.data[self.nodes.index(n)] = '.'

                print("Found solution in {} iterations.".format(iterations))
                return path

            # Avoid repeating
            reachable.remove(ne)
            explored.append(ne)

            # Where can we go from here?
            new_reachable = [n for n in ne.neighbours if n not in explored]
            for an in new_reachable:
                if an not in reachable:
                    reachable.append(an)

                new_cost = ne.get_cost() + 1
                if an.cost is None or new_cost < an.cost:
                    an.previous = ne
                    if ne.cost is None:
                        an.cost = 1
                    else:
                        an.cost = ne.cost + 1

            iterations += 1

        # If we get here, no path was found.
        return None


if __name__ == '__main__':
    g = grid(5, 5,
        '   # '
        's### '
        '     '
        '# ##e'
        '#    ')

    g.find_path()
    print(g)

    """
    g = grid(10, 10,
        's  # ### #'
        ' ##### # #'
        '    #    #'
        '  # # # ##'
        '# #   # # '
        '  ## ##   '
        '###  #  # '
        '     # ## '
        '# #  #  ##'
        '#    #e  #')

    g.find_path()
    print(g)
    
    g = grid(10, 10,
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
