import unittest
from hive.hexutil import *


class TestHexUtil(unittest.TestCase):
    def test_hexagon_distance_x(self):
        self.assertAlmostEqual(relative_distance_x(Point(0, 0), Point(0, 1)), math.sqrt(3) / 2, 5)
        self.assertAlmostEqual(relative_distance_x(Point(2, 3), Point(3, 3)), math.sqrt(3), 5)
        self.assertAlmostEqual(relative_distance_x(Point(2, 3), Point(1, 3)), -math.sqrt(3), 5)
        self.assertAlmostEqual(relative_distance_x(Point(2, 3), Point(4, 4)), math.sqrt(3) * 1.5, 5)
        self.assertAlmostEqual(relative_distance_x(Point(2, 3), Point(4, 5)), math.sqrt(3) * 2, 5)

    def test_hexagon_distance_y(self):
        self.assertAlmostEqual(relative_distance_y(Point(0, 0), Point(0, 1)), 1.5, 5)
        self.assertAlmostEqual(relative_distance_y(Point(0, 0), Point(1, 0)), 0, 5)
        self.assertAlmostEqual(relative_distance_y(Point(0, 0), Point(1, 1)), 1.5, 5)
        self.assertAlmostEqual(relative_distance_y(Point(1, 1), Point(2, 3)), 3, 5)
        self.assertAlmostEqual(relative_distance_y(Point(1, 1), Point(1, 5)), 6, 5)

    def test_hexagon_to_pixel(self):
        h = hexagon_to_pixel(Point(250, 250), Point(0, 1), 100)
        self.assertAlmostEqual(h.x, int(250 + math.sqrt(3) / 2 * 100.0))
        self.assertAlmostEqual(h.y, 250 + int(1.5 * 100.0))
        h = hexagon_to_pixel(Point(250, 250), Point(1, 0), 100)
        self.assertAlmostEqual(h.x, int(250 + math.sqrt(3) * 100.0))
        self.assertAlmostEqual(h.y, 250)
        h = hexagon_to_pixel(Point(250, 250), Point(0, 2), 100)
        self.assertAlmostEqual(h.x, 250)
        self.assertAlmostEqual(h.y, 250 + int(3 * 100.0))
