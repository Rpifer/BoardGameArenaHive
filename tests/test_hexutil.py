import unittest
from hive.hexutil import *


class TestHexUtil(unittest.TestCase):
    def test_hexagon_arithmetic(self):
        self.assertTrue(hexagon(4, -10, 6), hexagon_add(hexagon(1, -3, 2), hexagon(3, -7, 4)))
        self.assertTrue(equal_hexagon(hexagon(-2, 4, -2), hexagon_subtract(hexagon(1, -3, 2), hexagon(3, -7, 4))))

    def test_hexagon_direction(self):
        self.assertTrue(equal_hexagon(hexagon(0, -1, 1), hexagon_direction(2)))

    def test_hexagon_neighbor(self):
        self.assertTrue(equal_hexagon(hexagon(1, -3, 2), hexagon_neighbor(hexagon(1, -2, 1), 2)))
        self.assertEqual(1, 1)

    def test_hexagon_diagonal(self):
        self.assertTrue(equal_hexagon(hexagon(-1, -1, 2), hexagon_diagonal_neighbor(hexagon(1, -2, 1), 3)))

    def test_hexagon_distance(self):
        self.assertTrue(equal_int(7, hexagon_distance(hexagon(3, -7, 4), hexagon(0, 0, 0))))

    def test_hexagon_rotate_right(self):
        self.assertTrue(equal_hexagon(hexagon_rotate_right(hexagon(1, -3, 2)), hexagon(3, -2, -1)))

    def test_hexagon_rotate_left(self):
        self.assertTrue(equal_hexagon(hexagon_rotate_left(hexagon(1, -3, 2)), hexagon(-2, -1, 3)))

    def test_hexagon_round(self):
        a = hexagon(0.0, 0.0, 0.0)
        b = hexagon(1.0, -1.0, 0.0)
        c = hexagon(0.0, -1.0, 1.0)
        self.assertTrue(equal_hexagon(hexagon(5, -10, 5), hexagon_round(
            hexagon_line_interpolation(hexagon(0.0, 0.0, 0.0), hexagon(10.0, -20.0, 10.0), 0.5))))
        self.assertTrue(equal_hexagon(hexagon_round(a), hexagon_round(hexagon_line_interpolation(a, b, 0.499))))
        self.assertTrue(equal_hexagon(hexagon_round(b), hexagon_round(hexagon_line_interpolation(a, b, 0.501))))
        self.assertTrue(equal_hexagon(hexagon_round(a), hexagon_round(
            hexagon(a.q * 0.4 + b.q * 0.3 + c.q * 0.3, a.r * 0.4 + b.r * 0.3 + c.r * 0.3,
                    a.s * 0.4 + b.s * 0.3 + c.s * 0.3))))
        self.assertTrue(equal_hexagon(hexagon_round(c), hexagon_round(
            hexagon(a.q * 0.3 + b.q * 0.3 + c.q * 0.4, a.r * 0.3 + b.r * 0.3 + c.r * 0.4,
                    a.s * 0.3 + b.s * 0.3 + c.s * 0.4))))

    def test_hexagon_line_draw(self):
        self.assertTrue(equal_hexagon_array([hexagon(0, 0, 0), hexagon(0, -1, 1), hexagon(0, -2, 2),
                                            hexagon(1, -3, 2), hexagon(1, -4, 3), hexagon(1, -5, 4)],
                                            hexagon_line_draw(hexagon(0, 0, 0), hexagon(1, -5, 4))))

    def test_layout(self):
        h = hexagon(3, 4, -7)
        flat = Layout(layout_flat, Point(10.0, 15.0), Point(35.0, 71.0))
        self.assertTrue(equal_hexagon(h, hexagon_round(pixel_to_hexagon(flat, hexagon_to_pixel(flat, h)))))
        pointy = Layout(layout_pointy, Point(10.0, 15.0), Point(35.0, 71.0))
        self.assertTrue(equal_hexagon(h, hexagon_round(pixel_to_hexagon(pointy, hexagon_to_pixel(pointy, h)))))

    def test_offset_round_trip(self):
        a = hexagon(3, 4, -7)
        b = OffsetCoord(1, -3)
        self.assertTrue(equal_hexagon(a, q_offset_to_cube(EVEN, q_offset_from_cube(EVEN, a))))
        self.assertTrue(equal_offset_coord(b, q_offset_from_cube(EVEN, q_offset_to_cube(EVEN, b))))
        self.assertTrue(equal_hexagon(a, q_offset_to_cube(ODD, q_offset_from_cube(ODD, a))))
        self.assertTrue(equal_offset_coord(b, q_offset_from_cube(ODD, q_offset_to_cube(ODD, b))))
        self.assertTrue(equal_hexagon(a, r_offset_to_cube(EVEN, r_offset_from_cube(EVEN, a))))
        self.assertTrue(equal_offset_coord(b, r_offset_from_cube(EVEN, r_offset_to_cube(EVEN, b))))
        self.assertTrue(equal_hexagon(a, r_offset_to_cube(ODD, r_offset_from_cube(ODD, a))))
        self.assertTrue(equal_offset_coord(b, r_offset_from_cube(ODD, r_offset_to_cube(ODD, b))))

    def test_offset_from_cube(self):
        self.assertTrue(equal_offset_coord(OffsetCoord(1, 3), q_offset_from_cube(EVEN, hexagon(1, 2, -3))))
        self.assertTrue(equal_offset_coord(OffsetCoord(1, 2), q_offset_from_cube(ODD, hexagon(1, 2, -3))))

    def test_offset_to_cube(self):
        self.assertTrue(equal_hexagon(hexagon(1, 2, -3), q_offset_to_cube(EVEN, OffsetCoord(1, 3))))
        self.assertTrue(equal_hexagon(hexagon(1, 2, -3), q_offset_to_cube(ODD, OffsetCoord(1, 2))))

    def test_doubled_round_trip(self):
        a = hexagon(3, 4, -7)
        b = DoubledCoord(1, -3)
        self.assertTrue(equal_hexagon(a, q_doubled_to_cube(q_doubled_from_cube(a))))
        self.assertTrue(equal_doubled_coord(b, q_doubled_from_cube(q_doubled_to_cube(b))))
        self.assertTrue(equal_hexagon(a, r_doubled_to_cube(r_doubled_from_cube(a))))
        self.assertTrue(equal_doubled_coord(b, r_doubled_from_cube(r_doubled_to_cube(b))))

    def test_doubled_from_cube(self):
        self.assertTrue(equal_doubled_coord(DoubledCoord(1, 5), q_doubled_from_cube(hexagon(1, 2, -3))))
        self.assertTrue(equal_doubled_coord(DoubledCoord(4, 2), r_doubled_from_cube(hexagon(1, 2, -3))))

    def test_doubled_to_cube(self):
        self.assertTrue(equal_hexagon(hexagon(1, 2, -3), q_doubled_to_cube(DoubledCoord(1, 5))))
        self.assertTrue(equal_hexagon(hexagon(1, 2, -3), r_doubled_to_cube(DoubledCoord(4, 2))))


def equal_hexagon(a, b):
    return a.q == b.q and a.s == b.s and a.r == b.r


def equal_offset_coord(a, b):
    return a.col == b.col and a.row == b.row


def equal_doubled_coord(a, b):
    return a.col == b.col and a.row == b.row


def equal_int(a, b):
    return a == b


def equal_hexagon_array(a, b):
    result = equal_int(len(a), len(b))
    for i in range(0, len(a)):
        result = result and equal_hexagon(a[i], b[i])
    return result
