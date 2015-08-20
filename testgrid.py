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
        for node in path:
            print('{}: {} x {}'.format(path.index(node), node.x, node.y))

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

        path = g.find_path((0, 0), (6, 9))
        print(g)
        for node in path:
            print('{}: {} x {}'.format(path.index(node), node.x, node.y))

    def testGrid3(self):
        g = Grid(10, 2,
            '    ww    '
            '      ww  ')

        path = g.find_path((0, 1), (9,1))
        print(g)
        for node in path:
            print('{}: {} x {}'.format(path.index(node), node.x, node.y))

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
        for node in path:
            print('{}: {} x {}'.format(path.index(node), node.x, node.y))

    def testGrid5(self):
        g = Grid(30, 17,
            #0        1         2         3
            #123456789012345678901234567890
            '##############################' # 1
            '#                            #' # 2
            '# #####                 #### #' # 3
            '# ##                      ## #' # 4
            '# #                        # #' # 5
            '#                            #' # 6
            '#                            #' # 7
            '#                            #' # 8
            '#                            #' # 9
            '#                            #' # 10
            '#                            #' # 11
            '#                            #' # 12
            '# #                        # #' # 13
            '# ##                      ## #' # 14
            '# ####                  #### #' # 15
            '#                            #' # 16
            '##############################') # 17
      
        # path = g.find_path((1,1), (20,10))
        path = g.find_path((1,1, ), (5,1,))
        print(g)

        #for node in g.nodes:
        #    print(node)

        for node in path:
            print('{}: {} x {}'.format(path.index(node), node.x, node.y))

if __name__ == '__main__':
    unittest.main()
