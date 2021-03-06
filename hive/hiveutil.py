from hive import piece, board, hexutil
from typing import List, Any
from collections import deque, namedtuple
import math

Move = namedtuple("Move", ["position", "direction"])


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


def generate_hive_movement_cloud(tiles: List[board.Tile], mover):
    possible_spots = []
    for tile in tiles:
        neighbors = hexutil.touching_hexagons(hexutil.Point(tile.x, tile.y))
        for n in neighbors:
            if n in possible_spots:
                continue
            match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y
                          and tiles[i].z == mover.z), None)
            # if tile not occupied
            if match is None:
                possible_spots.append(n)
    return possible_spots


def generate_valid_moves(moving: board.Tile, tiles: List[board.Tile]):
    temp = tiles[:]
    if moving in temp:
        temp.remove(moving)
    full_space_without_mover = generate_hive_movement_cloud(temp, moving)
    possible_moves = []
    for possible_move in full_space_without_mover:
        if moving.piece.can_crawl and can_start_crawl(moving, tiles, moving.z):
            if space_crawable(moving, possible_move, tiles, full_space_without_mover):
                possible_moves.append(possible_move)
        if moving.piece.can_hop and can_start_hop(moving, tiles, moving.z):
            if space_hopable(moving, possible_move, tiles, full_space_without_mover):
                possible_moves.append(possible_move)

    return possible_moves
    # generate spots that it can go based on rules
    # confirm that it can get to each of those spots via movement rules
    # confirm that each space it will occupy is a valid hive


def space_crawable(start: board.Tile, end: hexutil.Point, tiles: List[board.Tile], movement_cloud):
    # todo: need to be able to work in 3d space
    possible_paths = [deque()]
    # todo: add z axis to Move object
    possible_paths[0].append(Move(hexutil.Point(start.x, start.y), 0))

    temp = tiles[:]
    if start in temp:
        temp.remove(start)

    current_path = possible_paths[0]
    spots = start.piece.crawl_spaces or 20
    for i in range(1, spots + 1):
        paths_to_extend = possible_paths[:]
        p: deque[Move]
        for p in paths_to_extend:
            path_to_be_removed = p
            neighbors = hexutil.touching_hexagons(p[-1].position)
            for n in neighbors:
                # todo: add z axis in can_slide check
                if n in movement_cloud and can_slide_to(p[-1].position, n, temp, start.z):
                    # not (dir != p[-1]dir and not p[-2].hex == n)
                    if len(p) >= 2 and p[-2].position == n:
                        continue
                    elif n == end and start.piece.crawl_spaces is None:
                        return True
                    # todo: add in z axis when adding new move (axis of start z, cannot change)
                    possible_paths.append(p + deque([Move(n, direction_of_crawl(p[-1].position, n, temp))]))
                    # at end and cannot be moved to
                elif n == end:
                    return False

            possible_paths.remove(path_to_be_removed)

    return any(move[-1].position == end for move in possible_paths)
    # return end in possible_paths[spots]
    # check closest path that can be reached via traversal rules, ie can slide


def space_hopable(start: board.Tile, end: hexutil.Point, tiles: List[board.Tile], movement_cloud):
    # determine if start and end are in the same line
    x_dist = hexutil.relative_distance_x(hexutil.Point(start.x, start.y), end)
    y_dist = hexutil.relative_distance_y(hexutil.Point(start.x, start.y), end)
    angle = angle_of_vector(x_dist, y_dist)
    if angle % 60 != 0:
        return False
    # determine if there are spaces open in that line
    match = -1
    space = start
    while end != space:
        n = hexutil.touching_hexagons(space)[int(angle / 60)]
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y), None)
        if match is None and end != n:
            return False
        space = n
    return True
    # if so and if not then yes


def direction_of_crawl(start: hexutil.Point, end: hexutil.Point, tiles: List[board.Tile]):
    # find neighbors of start
    start_neighbors = hexutil.touching_hexagons(start)
    # find neighbors of end
    end_neighbors = hexutil.touching_hexagons(end)
    # find union
    intersecting_neighbors = list(set(start_neighbors) & set(end_neighbors))
    static_piece = None
    # find one of those that is a piece
    for p in intersecting_neighbors:
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == p.x and tiles[i].y == p.y), None)
        if match is not None:
            static_piece = p
            break

    if static_piece is None:
        return 0  # not valid move
    # calculate angle of start and angle of end in relation to that piece
    x_start = hexutil.relative_distance_x(static_piece, start)
    y_start = hexutil.relative_distance_y(static_piece, start)
    x_end = hexutil.relative_distance_x(static_piece, end)
    y_end = hexutil.relative_distance_y(static_piece, end)
    # find angle of start
    t_start = angle_of_vector(x_start, y_start)
    t_end = angle_of_vector(x_end, y_end)
    return (1, -1)[t_end > t_start]  # if increasing, then counter clockwise then -1


def angle_of_vector(x, y):
    # backwards due to orientation of axis
    y = -y
    if y == 0:
        return int(x < 0) * 180

    if x == 0:
        return int(y > 0) * 180 + 90

    theta = math.degrees(math.atan(abs(y / x)))
    if x < 0 < y:
        theta = 180 - theta
    elif x < 0 and y < 0:
        theta += 180
    elif x > 0 > y:
        theta = 360 - theta

    return theta


def can_slide_to(start, end: hexutil.Point, tiles: List[board.Tile], z):
    """Assumes start is next to end, remove start before calling
    can slide if end has 2 continuous spaces AND start is in one of those spaces"""
    # todo, add in z axis for match checking
    match = next((i for i in range(0, len(tiles)) if tiles[i].x == end.x and tiles[i].y == end.y
                  and tiles[i].z == z), None)
    # todo, needs to be removed if on top of hive
    # cant slide there if something is already there
    if match is not None:
        return False

    # if it is a layer up, it NEEDS to have something there to be able to crawl there
    if z != 0:
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == end.x and tiles[i].y == end.y
                      and tiles[i].z == z - 1), None)
        if match is None:
            return False

    if direction_of_crawl(start, end, tiles) == 0 and z == 0:
        return False

    neighbors = hexutil.touching_hexagons(end)
    continuous_spaces = 0
    start_in_continuous = False
    for j in range(-1, len(neighbors)):
        n = neighbors[j]
        # todo, again add in z axis of start tiles
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y
                      and tiles[i].z == z), None)
        if match is not None:
            continuous_spaces = 0
            start_in_continuous = False
        else:
            continuous_spaces += 1
            if start == n:
                start_in_continuous = True
            if continuous_spaces >= 2 and start_in_continuous:
                return True
    return False


def can_start_crawl(start: hexutil.Point, tiles: List[board.Tile], z):
    # todo, probably going to need z axis here too
    neighbors = hexutil.touching_hexagons(hexutil.Point(start.x, start.y))
    touches = 0
    max_continuous_touches = 0
    continuous_touches = 0
    for n in neighbors:
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y
                      and tiles[i].z == z), None)
        if match is not None:
            touches += 1
            continuous_touches += 1
            max_continuous_touches = max(max_continuous_touches, continuous_touches)
        else:
            continuous_touches = 0

    if touches >= 5:
        return False
    if touches == max_continuous_touches:
        return True
    else:
        return False


def can_start_hop(start: hexutil.Point, tiles: List[board.Tile], z):
    neighbors = hexutil.touching_hexagons(hexutil.Point(start.x, start.y))
    touches = 0
    max_continuous_touches = 0
    continuous_touches = 0
    for n in neighbors:
        match = next((i for i in range(0, len(tiles)) if tiles[i].x == n.x and tiles[i].y == n.y
                      and tiles[i].z == z), None)
        if match is not None:
            touches += 1
            continuous_touches += 1
            max_continuous_touches = max(max_continuous_touches, continuous_touches)
        else:
            continuous_touches = 0

    if touches == max_continuous_touches:
        return True
    else:
        return False
