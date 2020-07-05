import unittest
from hive import hexutil, hiveutil, board, piece, game


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
        self.assertCountEqual(hiveutil.generate_hive_movement_cloud(t, t[0]), cloud)

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
        self.assertCountEqual(hiveutil.generate_hive_movement_cloud(t, t[0]), cloud)


class TestHiveUtilCanStartCrawl(unittest.TestCase):
    def test_can_start_crawl_two(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W'))
        ]

        self.assertTrue(hiveutil.can_start_crawl(t[0], t, t[0].z))

    def test_can_start_crawl_many(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(3, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 2, 0, piece.create_ladybug('W')),
            board.Tile(3, 3, 0, piece.create_ladybug('W')),
        ]

        self.assertTrue(hiveutil.can_start_crawl(t[0], t, t[0].z))

    def test_can_not_start_crawl_ring(self):
        t = [
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 2, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W')),
            board.Tile(0, 1, 0, piece.create_ladybug('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W'))
        ]

        self.assertFalse(hiveutil.can_start_crawl(t[0], t, t[0].z))

    def test_can_not_start_crawl_pinned(self):
        t = [
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(3, 0, 0, piece.create_ladybug('W'))
        ]

        self.assertFalse(hiveutil.can_start_crawl(t[1], t, t[0].z))


class TestHiveUtilCanSlide(unittest.TestCase):
    def test_can_slide_two(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W'))
        ]
        first = t.pop(0)
        self.assertTrue(hiveutil.can_slide_to(hexutil.Point(first.x, first.y), hexutil.Point(3, 0), t, first.z))

    def test_can_slide_many(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(3, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 2, 0, piece.create_ladybug('W')),
            board.Tile(3, 3, 0, piece.create_ladybug('W')),
        ]
        first = t.pop(0)
        self.assertTrue(hiveutil.can_slide_to(hexutil.Point(first.x, first.y), hexutil.Point(1, 1), t, first.z))

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
        first = t.pop(0)
        self.assertFalse(hiveutil.can_slide_to(hexutil.Point(first.x, first.y), hexutil.Point(3, 1), t, first.z))


class TestHiveUtilSpaceCrawable(unittest.TestCase):
    def test_can_crawl_to_beetle(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_beetle('W'))
        self.assertTrue(hiveutil.space_crawable(p,
                                                hexutil.Point(0, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_crawl_to_beetle_on_top(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(1, 0, 1, piece.create_beetle('W'))
        self.assertTrue(hiveutil.space_crawable(p,
                                                hexutil.Point(1, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_beetle_on_top_too_far(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(1, 1, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(1, 0, 1, piece.create_beetle('W'))
        self.assertFalse(hiveutil.space_crawable(p,
                                                hexutil.Point(1, 2), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_beetle__on_top_gate(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ladybug('W')),
            board.Tile(-1, -1, 0, piece.create_ladybug('W')),
            board.Tile(-1, -1, 1, piece.create_beetle('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(0, -1, 0, piece.create_ladybug('W')),
            board.Tile(0, -1, 1, piece.create_beetle('W')),
        ]
        p = board.Tile(0, 0, 1, piece.create_beetle('W'))
        self.assertFalse(hiveutil.space_crawable(p,
                                                hexutil.Point(0, -1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_beetle_out_of_range(self):
        t = [

            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_beetle('W'))
        self.assertFalse(hiveutil.space_crawable(p,
                                                 hexutil.Point(1, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_crawl_to_ant(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_ant('W'))
        self.assertTrue(hiveutil.space_crawable(p
                                                , hexutil.Point(1, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_ant_gates(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 2, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_ant('W'))
        self.assertFalse(hiveutil.space_crawable(p,
                                                 hexutil.Point(1, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_crawl_to_ant_gates_in_big_ring(self):
        t = [
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(3, 0, 0, piece.create_ladybug('W')),
            board.Tile(4, 0, 0, piece.create_ladybug('W')),
            board.Tile(4, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 2, 0, piece.create_ladybug('W')),
            board.Tile(3, 3, 0, piece.create_ladybug('W')),
            board.Tile(2, 3, 0, piece.create_ladybug('W')),
            board.Tile(1, 3, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W'))
        ]
        p = board.Tile(1, 0, 0, piece.create_ant('W'))
        self.assertTrue(hiveutil.space_crawable(p
                                                , hexutil.Point(3, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_ant_gates_in_big_ring(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(3, 0, 0, piece.create_ladybug('W')),
            board.Tile(4, 0, 0, piece.create_ladybug('W')),
            board.Tile(4, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 2, 0, piece.create_ladybug('W')),
            board.Tile(3, 3, 0, piece.create_ladybug('W')),
            board.Tile(2, 3, 0, piece.create_ladybug('W')),
            board.Tile(1, 3, 0, piece.create_ladybug('W')),
            board.Tile(1, 2, 0, piece.create_ladybug('W'))
        ]
        p = board.Tile(0, 0, 0, piece.create_ant('W'))
        self.assertFalse(hiveutil.space_crawable(p
                                                 , hexutil.Point(3, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_crawl_to_spider(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_spider('W'))
        self.assertTrue(hiveutil.space_crawable(p,
                                                hexutil.Point(2, 0), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_spider_two_space(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_spider('W'))
        self.assertFalse(hiveutil.space_crawable(p,
                                                 hexutil.Point(1, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_crawl_to_spider_back_and_forth(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_spider('W'))
        self.assertFalse(hiveutil.space_crawable(p,
                                                 hexutil.Point(0, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_crawl_to_spider_strange_case(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(2, 2, 0, piece.create_ladybug('W')),
            board.Tile(1, 3, 0, piece.create_ladybug('W')),
            board.Tile(0, 3, 0, piece.create_ladybug('W')),
            board.Tile(0, 2, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_spider('W'))
        cloud = hiveutil.generate_hive_movement_cloud(t, p)
        self.assertTrue(hiveutil.space_crawable(p
                                                , hexutil.Point(1, 2), t, cloud))
        self.assertTrue(hiveutil.space_crawable(p,
                                                hexutil.Point(1, 1), t, cloud))
        self.assertTrue(hiveutil.space_crawable(p,
                                                hexutil.Point(2, -1), t, cloud))
        self.assertTrue(hiveutil.space_crawable(p,
                                                hexutil.Point(-1, 2), t, cloud))


class TestHiveUtilGenerateValidMoves(unittest.TestCase):
    def test_valid_moves_single_ant(self):
        t = [
            board.Tile(0, 0, 0, piece.create_ant('W')),
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        moves = hexutil.touching_hexagons(hexutil.Point(1, 0))
        self.assertCountEqual(hiveutil.generate_valid_moves(t[0], t), moves)


class TestHiveUtilSpaceHopable(unittest.TestCase):
    def test_can_hop_hopper_simple(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_hopper('B'))
        self.assertTrue(hiveutil.space_hopable(p, hexutil.Point(2, 0), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_hop_hopper_simple_off_direction(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_hopper('B'))
        self.assertFalse(hiveutil.space_hopable(p, hexutil.Point(1, 1), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_hop_hopper_long(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(3, 0, 0, piece.create_ladybug('W')),
            board.Tile(4, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_hopper('B'))
        self.assertTrue(hiveutil.space_hopable(p, hexutil.Point(5, 0), t, hiveutil.generate_hive_movement_cloud(t, p)))

    def test_can_not_hop_hopper_space(self):
        t = [
            board.Tile(1, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 0, 0, piece.create_ladybug('W')),
            board.Tile(2, 1, 0, piece.create_ladybug('W')),
            board.Tile(3, 1, 0, piece.create_ladybug('W')),
            board.Tile(4, 0, 0, piece.create_ladybug('W')),
        ]
        p = board.Tile(0, 0, 0, piece.create_hopper('B'))
        self.assertFalse(hiveutil.space_hopable(p, hexutil.Point(5, 0), t, hiveutil.generate_hive_movement_cloud(t, p)))
        self.assertTrue(hiveutil.space_hopable(p, hexutil.Point(3, 0), t, hiveutil.generate_hive_movement_cloud(t, p)))