from hive import piece, hexutil
import collections

Tile = collections.namedtuple("Tile", ["x", "y", "z", "piece"])


class Board:
    def __init__(self):
        self.play_space = {(0, 0): [None]}

    def add_piece(self, x, y, p):
        z = 0
        while self.space_occupied(x, y, z):
            z = z + 1

        if self.coordinate_exists(x, y, z):
            if self.space_occupied(x, y, z):
                self.play_space[(x, y)].insert(z, p)
            elif z == 0:
                self.play_space[(x, y)].pop() # remove placeholder None
                self.play_space[(x, y)].insert(z, p)
        else:
            self.play_space[(x, y)] = [p]

    def move_piece(self, old_x, old_y, new_x, new_y):
        old_piece = self.play_space[old_x, old_y].pop()
        self.add_piece(new_x, new_y, old_piece)

    def piece_at(self, x, y, z):
        return self.play_space[(x, y)][z]

    def coordinate_exists(self, x, y, z):
        return (x, y) in self.play_space and z < len(self.play_space[(x, y)])

    def space_occupied(self, x, y, z=0):
        return self.coordinate_exists(x, y, z) and self.piece_at(x, y, z) is not None

    def get_occupied_tiles(self):
        tiles = []
        for p in self.play_space.items():
            point = hexutil.Point(p[0][0], p[0][1])
            if self.space_occupied(point.x, point.y, 0):
                for z in range(0, len(p[1])):
                    tiles.append(Tile(point.x, point.y, z, self.piece_at(point.x, point.y, z)))
        tiles.sort(key=lambda tile: (tile.x, tile.y, tile.z))
        return tiles
