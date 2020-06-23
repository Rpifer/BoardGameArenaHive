import sys

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
        self.mimic_piece = None
        self.crawl_spaces = 1


def create_ant(color):
    p = Piece(color, 'ANT')
    p.can_crawl = True
    p.crawl_spaces = None


def create_spider(color):
    p = Piece(color, 'SPIDER')
    p.can_crawl = True
    p.crawl_spaces = 3

def create_hopper(color):
    p = Piece(color, 'HOPPER')
    p.can_crawl = True
    p.crawl_spaces = 3

