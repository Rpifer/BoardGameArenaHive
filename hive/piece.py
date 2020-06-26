import random

class Piece:
    def __init__(self, color, species):
        self.color = color
        self.species = species
        self.can_climb = False
        self.can_hop = False
        self.can_zap = False
        self.can_traverse = False
        self.can_mimic = False
        self.can_crawl = False
        self.crawl_spaces = 1


def create_rand_piece():
    r = random.randint(1, 8)
    if r == 1:
        return create_ant(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 2:
        return create_spider(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 3:
        return create_queen(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 4:
        return create_ladybug(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 5:
        return create_mosquito(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 6:
        return create_beetle(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 7:
        return create_hopper(("W", "B")[random.randrange(1, 3) % 2 == 0])
    if r == 8:
        return create_pill( ("W", "B")[random.randrange(1, 3) % 2 == 0])


def create_ant(color):
    p = Piece(color, 'A')
    p.can_crawl = True
    p.crawl_spaces = None
    return p


def create_spider(color):
    p = Piece(color, 'S')
    p.can_crawl = True
    p.crawl_spaces = 3
    return p


def create_queen(color):
    p = Piece(color, 'Q')
    p.can_crawl = True
    p.crawl_spaces = 1
    return p


def create_hopper(color):
    p = Piece(color, 'H')
    p.can_hop = True
    p.crawl_space = 0
    return p


def create_beetle(color):
    p = Piece(color, 'B')
    p.can_climb = True
    p.can_crawl = True
    p.crawl_space = 1
    return p


def create_pill(color):
    p = Piece(color, 'P')
    p.can_zap = True
    p.can_crawl = True
    p.crawl_space = 1
    return p


def create_ladybug(color):
    p = Piece(color, 'L')
    p.can_traverse = True
    p.crawl_space = 0
    return p


def create_mosquito(color):
    p = Piece(color, 'M')
    p.can_mimic = True
    p.crawl_space = 0
    return p


def create_reserve(color, m=True, p=True, l=True):
    reserve = [create_queen(color),
               create_ant(color), create_ant(color), create_ant(color),
               create_hopper(color), create_hopper(color), create_hopper(color),
               create_spider(color), create_spider(color),
               create_beetle(color), create_beetle(color)
               ]
    if m:
        reserve.append(create_mosquito(color))
    if p:
        reserve.append(create_pill(color))
    if l:
        reserve.append(create_ladybug(color))

    return reserve


