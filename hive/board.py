from hive import piece
from hive import hexutil
import math


class Space(object):
    def __init__(self, h: hexutil.Hexagon, p: piece.Piece):
        self._tile = h
        self.piece = p

    @property
    def tile(self):
        return self._tile


class Board:
    def __init__(self):
        self.play_space = {(0, 0, 0): Space(hexutil.hexagon(0, 0), None)}

    def add_piece(self, x, y, p: piece.Piece):
        z = 0
        while (x, y, z) in self.play_space and self.play_space[(x, y, z)].piece is not None:
            z = z + 1

        if (x, y, z) in self.play_space and self.play_space[(x, y, z)].piece is None:
            self.play_space[(x, y, z)].piece = p
        else:
            self.play_space[(x, y, z)] = Space(hexutil.hexagon(x, y), p)

    def piece_at(self, x, y, z):
        return self.play_space[(x, y, z)].piece

    def tile_at(self, x, y):
        return self.play_space[(x, y, 0)].tile

    def space_occupied(self, h: hexutil.Hexagon):
        return (h.q, h.r, 0) in self.play_space and self.play_space[(h.q, h.r, 0)] is not None

    def get_bounding_limits(self):
        """
        :rtype: hexutil.Point, hexutil.Point
        """
        min_x, max_x, min_y, max_y = 0
        for h in self.play_space.items():
            tile = h[1].tile
            min_x = min(tile.q, min_x)
            max_x = max(tile.q, max_x)
            min_y = min(tile.r, min_y)
            max_y = max(tile.r, max_y)
        return hexutil.Point(min_x, min_y), hexutil.Point(max_x, max_y)





