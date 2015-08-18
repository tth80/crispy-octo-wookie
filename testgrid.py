import unittest
from grid import Grid, Node

class NodeTest(unittest.TestCase):
    def testCoords(self):
        n = Node(0, 0)
        self.assertEqual(0, n.x)
        self.assertEqual(0, n.y)
        
        n2 = Node(10, 10)
        self.assertEqual(10, n2.x)
        self.assertEqual(10, n2.y)


class GridTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGrid(self):
        g = Grid(5, 5,
            '   # '
            ' ### '
            '     '
            '# ## '
            '#    ')

        path = g.find_path((0, 1), (4,3))
        print(g)

        self.assertEqual(len(g.data), 5*5)

    def testGrid2(self):
        g = Grid(10, 10,
            '   # ### #'
            ' ##### # #'
            '    #    #'
            '  # # # ##'
            '# #   # # '
            '  ## ##   '
            '###  w  # '
            '     # ## '
            '# #  #  ##'
            '#    #   #')

        g.find_path((0, 0), (6, 9))
        print(g)

    def testGrid3(self):
        g = Grid(10, 2,
            '    ww    '
            '      ww  ')

        g.find_path((0, 1), (9,1))
        print(g)

        """
        for n in g.nodes:
            print('node {0} cost {2}: cost_so_far: {1}'.format(n.index, n.cost_so_far, n.cost))
        """

    def testGrid4(self):
        g = Grid(10, 10,
            '          '
            '          '
            '          '
            '          '
            '          '
            '          '
            '        # '
            '       ## '
            '      ##  '
            '     w w  ')

        path = g.find_path((5, 6), (8, 8))
        print(g)


if __name__ == '__main__':
    unittest.main()
