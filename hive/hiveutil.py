from hive import piece, board, hexutil
from typing import List


def is_one_hive(tiles: List[board.Tile]):
    tiles_count = len(tiles)
    main_hive = []
    if len(tiles) <= 1:
        return True

    main_tile = tiles.pop(0)
    main_hive.append(main_tile)
    stop = False
    actual_tiles = []
    while not stop:
        possible_tiles = hexutil.touching_hexagons(hexutil.Point(main_tile.x, main_tile.y))
        # check for above piece
        possible_tiles.append(hexutil.Point(main_tile.x, main_tile.y))
        for tile in possible_tiles:
            match = next((i for i in range(0, len(tiles)) if tiles[i].x == tile.x and tiles[i].y == tile.y), None)
            if match is not None:
                touching_tile = tiles.pop(match)
                actual_tiles.append(touching_tile)
                main_hive.append(touching_tile)
        if len(actual_tiles) != 0:
            main_tile = actual_tiles.pop(0)
        else:
            stop = True

    return tiles_count == len(main_hive)


def generate_hive_movement_cloud(tiles: List[board.Tile]):
    possible_spots = []
    for tile in tiles:
        neighbors = hexutil.touching_hexagons(hexutil.Point(tile.x, tile.y))
        for n in neighbors:
            if n in possible_spots:
                continue
            match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y), None)
            # if tile not occupied
            if match is None:
                possible_spots.append(n)
    return possible_spots


def generate_valid_moves(moving: board.Tile, tiles: List[board.Tile]):
    full_space = generate_hive_movement_cloud(tiles)
    possible_moves = []
    if moving.piece.can_crawl:
        for possible_move in full_space:
            if hex_crawable(moving, possible_move, tiles, full_space):
                possible_moves.append(possible_move)
    # generate spots that it can go based on rules
    # confirm that it can get to each of those spots via movement rules
    # confirm that each space it will occupy is a valid hive


def hex_crawable(start: board.Tile, end: board.Tile, tiles: List[board.Tile], movement_cloud):
    tiles = tiles[:]  # duplicate so to not change original
    # remove self from tiles to not interfere with movement
    tiles.remove(start)
    possible_paths = [[hexutil.Point(start.x, start.y)]]
    visited = [hexutil.Point(start.x, start.y)]

    spots = start.piece.crawl_spaces or 10000
    for i in range(1, start.piece.crawl_spaces):
        for p in possible_paths[i-1]:
            neighbors = hexutil.touching_hexagons(p)
            for n in neighbors:
                if n in movement_cloud:
                    return True

    # get neighbors of start,
    # if can slide to and in movement cloud
        # add to possible path

    return True
    # check closest path that can be reached via traversal rules, ie can slide


def can_slide_to(start: hexutil.Point, end: hexutil.Point, tiles: List[board.Tile]):
    """Assumes start is next to end, remove start before calling"""
    match = next((i for i in range(0, len(tiles)) if tiles[i].x == end.x and tiles[i].y == end.y), None)
    # can slide there if something is already there
    if match is not None:
        return False

    neighbors = hexutil.touching_hexagons(hexutil.Point(start.x, start.y))
    touches = 0
    max_continuous_touches = 0
    continuous_touches = 0
    for n in neighbors:
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y), None)
        if match is not None:
            touches += 1
            continuous_touches += 1
            max_continuous_touches = max(max_continuous_touches, continuous_touches)
        else:
            continuous_touches = 0

    if touches >= 5:
        return False
    if touches == continuous_touches:
        return True
    else:
        return False
    # can slide if up to 4 continous pieces are touching
    # cannot slide if 5 pieces are touching
    # cannot slide if 2 - 4 non continous pieces are touching it
