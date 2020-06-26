import unittest
from hive import hexutil, hiveutil, board, piece


class TestHiveUtilIsOneHive(unittest.TestCase):
    def test_is_one_hive_zero(self):
        t = [
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_one_hive_one(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W'))
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_one_hive_two_negative(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(-1, 0, 0, piece.create_ladybug('W'))
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_one_hive_two(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W'))
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_one_hive_two_z_axis(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(0, 0, 1, piece.create_beetle('W'))
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_one_hive_four(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_beetle('W')),
            board.Tile(1, 1, 0, piece.create_beetle('W')),
            board.Tile(1, 2, 0, piece.create_beetle('W'))
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_not_one_hive_two(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W'))
        ]
        self.assertFalse(hiveutil.is_one_hive(t))

    def test_is_not_one_hive_four(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 2, 0, piece.create_ladybug('W'))
        ]
        self.assertFalse(hiveutil.is_one_hive(t))

    def test_is_one_hive_eleven(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(3, 0, 0, piece.create_ladybug('W')),
            board.Tile(3, -1, 0, piece.create_ladybug('W')),
            board.Tile(3, -1, 0, piece.create_ladybug('W')),
            board.Tile(4, 0, 0, piece.create_ladybug('W')),
            board.Tile(4, 1, 0, piece.create_ladybug('W')),
        ]
        self.assertTrue(hiveutil.is_one_hive(t))

    def test_is_not_one_hive_eleven(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(3, 0, 0, piece.create_ladybug('W')),
            board.Tile(3, -1, 0, piece.create_ladybug('W')),
            board.Tile(3, -1, 0, piece.create_ladybug('W')),
            board.Tile(4, 0, 0, piece.create_ladybug('W')),
            board.Tile(5, 1, 0, piece.create_ladybug('W')),
        ]
        self.assertFalse(hiveutil.is_one_hive(t))


class TestHiveUtilHiveMovementCloud(unittest.TestCase):
    def test_movement_cloud_one_piece(self):
        t = [
            board.Tile(1, 1, 0, piece.create_ladybug('W'))
        ]
        cloud = [
            hexutil.Point(2, 0),
            hexutil.Point(2, 1),
            hexutil.Point(2, 2),
            hexutil.Point(1, 2),
            hexutil.Point(0, 1),
            hexutil.Point(1, 0),
        ]
        self.assertCountEqual(hiveutil.generate_hive_movement_cloud(t), cloud)

    def test_movement_cloud_six_piece_ring(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 2, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        cloud = [
            hexutil.Point(1, 1),
            hexutil.Point(3, 1),
            hexutil.Point(3, 2),
            hexutil.Point(2, 3),
            hexutil.Point(1, 3),
            hexutil.Point(0, 3),
            hexutil.Point(0, 2),
            hexutil.Point(-1, 1),
            hexutil.Point(0, 0),
            hexutil.Point(0, -1),
            hexutil.Point(1, -1),
            hexutil.Point(2, -1),
            hexutil.Point(3, 0),
        ]
        self.assertCountEqual(hiveutil.generate_hive_movement_cloud(t), cloud)


class TestHiveUtilCanSlide(unittest.TestCase):
    def test_can_slide_two(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W'))
        ]

        self.assertTrue(hiveutil.can_slide_to(t[0], hexutil.Point(3, 0), t))

    def test_can_slide_many(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(3, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 2, 0, piece.create_ladybug('W')),
            board.Tile(3, 3, 0, piece.create_ladybug('W')),
        ]

        self.assertTrue(hiveutil.can_slide_to(t[0], hexutil.Point(1, 1), t))

    def test_can_not_slide_ring(self):
        t = [
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 2, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]

        self.assertFalse(hiveutil.can_slide_to(t[0], hexutil.Point(3, 1), t))
