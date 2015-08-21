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

    def testInit(self):
        with self.assertRaises(TypeError):
            n = Node('1', 2)
        
        n = Node(int('1'), 2)
        n = Node(1, 2, cost=1)

        with self.assertRaises(TypeError):
            n = Node(1, 2, cost='a')

        n2 = Node(1, 2, previous=n)
        with self.assertRaises(TypeError):
            n = Node(1, 2, previous='a')

        n = Node(98123, 19238, neighbours=[n2])
        self.assertEqual('[98123,19238]', str(n))

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
        self.assertEqual([[4,3], [4,2], [3,2], [2,2], [1,2], [0,2]], 
                [[n.x, n.y] for n in path])
        self.assertEqual(len(g.data), 5*5)

        g.reset()
        for n in g.nodes:
            self.assertEqual(0, n.cost_so_far)

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
        self.assertEqual([
            [6,9], [6,8], [6,7], [6,6], [5,6], [4,6], [4,5], [4,4], 
            [3,4], [3,3], [3,2], [2,2], [1,2], [0,2], [0,1]],
            [[n.x, n.y] for n in path])
        self.assertEqual(len(g.data), 10*10)

    def testGrid3(self):
        g = Grid(10, 2,
            '    ww    '
            '      ww  ')

        path = g.find_path((0, 1), (9,1))
        self.assertEqual(
            [[9,1], [8,1], [7,1], [6,1], [5,1], [4,1], [3,1], [2,1], [1,1]],
            [[n.x, n.y] for n in path])
        self.assertEqual(len(g.data), 10*2)

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

        self.assertEqual([[8,8], [8,9], [7,9], [6,9], [5,9], [5,8], [5,7]],
            [[n.x, n.y] for n in path])
        self.assertEqual(len(g.data), 10*10)

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
        self.assertEqual([[5,1], [4,1], [3,1], [2,1]],
            [[n.x, n.y] for n in path])
        self.assertEqual(len(g.data), 30*17)

if __name__ == '__main__':
    unittest.main()
