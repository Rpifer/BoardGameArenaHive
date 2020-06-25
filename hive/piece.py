import uuid

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
        self.id = uuid.uuid1()


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


