import collections
import math
from typing import List

Point = collections.namedtuple("Point", ["x", "y"])


def relative_distance_x(p1: Point, p2: Point):
    distance = 0
    delta_point = Point(p2.x - p1.x, p2.y - p1.y)
    if p2.y % 2 == p1.y % 2:
        # no offset needed
        distance = 0
    elif p2.y % 2 == 0 and p1.y % 2 != 0:
        # offset backwards
        distance -= math.sqrt(3) / 2
    elif p2.y % 2 != 0 and p1.y % 2 == 0:
        # offset forwards
        distance += math.sqrt(3) / 2

    # add rest of x change
    distance += math.sqrt(3) * delta_point.x
    return distance


def relative_distance_y(p1: Point, p2: Point):
    distance = 0
    delta_point = Point(p2.x - p1.x, p2.y - p1.y)
    distance += delta_point.y * 1.5
    return distance

def hexagon_to_pixel(origin_pixel: Point, p: Point, side_length):
    x = relative_distance_x(Point(0, 0), p) * side_length
    y = relative_distance_y(Point(0, 0), p) * side_length
    return Point(int(x + origin_pixel.x), int(y + origin_pixel.y))


def pixel_to_closest_hexagon(origin_pixel, p: Point, side_length):
    relative_point = Point(p.x - origin_pixel.x, p.y - origin_pixel.y)
    base_hex = Point(relative_point.x // side_length, relative_point.y // side_length)
    dist = math.sqrt(abs(relative_point.x - relative_distance_x(Point(0, 0), base_hex) * side_length) ** 2
                     + abs(relative_point.y - relative_distance_y(Point(0, 0), base_hex) * side_length) ** 2)

    estimate_hex = base_hex

    if dist < side_length * math.sqrt(3) / 2:
        return estimate_hex

    for i in [0, 1, -1, 2, -2, 3, -3]:
        for j in [0, 1, -1, 2, -2, 3, -3]:
            if i == j == 0:
                continue
            estimate_hex = Point(base_hex.x + i, base_hex.y + j)
            dist = math.sqrt(abs(relative_point.x - relative_distance_x(Point(0, 0), estimate_hex) * side_length) ** 2
                             + abs(relative_point.y - relative_distance_y(Point(0, 0), estimate_hex) * side_length) ** 2)
            if dist < side_length * math.sqrt(3) / 2:
                return estimate_hex
    return None


def polygon_corners(origin_pixel: Point, p: Point, side_length):
    corners = []
    center = hexagon_to_pixel(origin_pixel, p, side_length)
    for i in range(0, 6):
        offset = hexagon_corner_offset(i, side_length)
        corners.append(Point(center.x + offset.x, center.y + offset.y))
    return corners


def hexagon_corner_offset(corner, side_length):
    angle = math.radians(corner * 60 + 30)
    return Point(side_length * math.cos(angle), side_length * math.sin(angle))

# # Generated code -- CC0 -- No Rights Reserved -- http://www.redblobgames.com/grids/hexagons/
#  OLD HEX UTIL
#
# import collections
# import math
#
#
#
# Hexagon = collections.namedtuple("Hexagon", ["q", "r", "s"])
#
#
# def hexagon(q, r, s=None):
#     if s is None:
#         s = 0 - q - r
#     assert not (round(q + r + s) != 0), "q + r + s must be 0"
#     return Hexagon(q, r, s)
#
#
# def hexagon_add(a, b):
#     return hexagon(a.q + b.q, a.r + b.r, a.s + b.s)
#
#
# def hexagon_subtract(a, b):
#     return hexagon(a.q - b.q, a.r - b.r, a.s - b.s)
#
#
# def hexagon_scale(a, k):
#     return hexagon(a.q * k, a.r * k, a.s * k)
#
#
# def hexagon_rotate_left(a):
#     return hexagon(-a.s, -a.q, -a.r)
#
#
# def hexagon_rotate_right(a):
#     return hexagon(-a.r, -a.s, -a.q)
#
#
# hexagon_directions = [hexagon(1, 0, -1), hexagon(1, -1, 0), hexagon(0, -1, 1), hexagon(-1, 0, 1), hexagon(-1, 1, 0),
#                       hexagon(0, 1, -1)]
#
#
# def hexagon_direction(direction):
#     return hexagon_directions[direction]
#
#
# def hexagon_neighbor(starting_hex, direction):
#     return hexagon_add(starting_hex, hexagon_direction(direction))
#
#
# hexagon_diagonals = [hexagon(2, -1, -1), hexagon(1, -2, 1), hexagon(-1, -1, 2), hexagon(-2, 1, 1), hexagon(-1, 2, -1),
#                      hexagon(1, 1, -2)]
#
#
# def hexagon_diagonal_neighbor(starting_hexagon, direction):
#     return hexagon_add(starting_hexagon, hexagon_diagonals[direction])
#
#
# def hexagon_length(starting_hexagon):
#     return (abs(starting_hexagon.q) + abs(starting_hexagon.r) + abs(starting_hexagon.s)) // 2
#
#
# def hexagon_distance(a, b):
#     return hexagon_length(hexagon_subtract(a, b))
#
#
# def hexagon_round(h):
#     qi = int(round(h.q))
#     ri = int(round(h.r))
#     si = int(round(h.s))
#     q_diff = abs(qi - h.q)
#     r_diff = abs(ri - h.r)
#     s_diff = abs(si - h.s)
#     if q_diff > r_diff and q_diff > s_diff:
#         qi = -ri - si
#     else:
#         if r_diff > s_diff:
#             ri = -qi - si
#         else:
#             si = -qi - ri
#     return hexagon(qi, ri, si)
#
#
# def hexagon_line_interpolation(a, b, t):
#     return hexagon(a.q * (1.0 - t) + b.q * t, a.r * (1.0 - t) + b.r * t, a.s * (1.0 - t) + b.s * t)
#
#
# def hexagon_line_draw(a, b):
#     n = hexagon_distance(a, b)
#     a_nudge = hexagon(a.q + 1e-06, a.r + 1e-06, a.s - 2e-06)
#     b_nudge = hexagon(b.q + 1e-06, b.r + 1e-06, b.s - 2e-06)
#     results = []
#     step = 1.0 / max(n, 1)
#     for i in range(0, n + 1):
#         results.append(hexagon_round(hexagon_line_interpolation(a_nudge, b_nudge, step * i)))
#     return results
#
#
# OffsetCoord = collections.namedtuple("OffsetCoord", ["col", "row"])
#
# EVEN = 1
# ODD = -1
#
#
# def q_offset_from_cube(offset, h):
#     col = h.q
#     row = h.r + (h.q + offset * (h.q & 1)) // 2
#     if offset != EVEN and offset != ODD:
#         raise ValueError("offset must be EVEN (+1) or ODD (-1)")
#     return OffsetCoord(col, row)
#
#
# def q_offset_to_cube(offset, h):
#     q = h.col
#     r = h.row - (h.col + offset * (h.col & 1)) // 2
#     s = -q - r
#     if offset != EVEN and offset != ODD:
#         raise ValueError("offset must be EVEN (+1) or ODD (-1)")
#     return hexagon(q, r, s)
#
#
# def r_offset_from_cube(offset, h):
#     col = h.q + (h.r + offset * (h.r & 1)) // 2
#     row = h.r
#     if offset != EVEN and offset != ODD:
#         raise ValueError("offset must be EVEN (+1) or ODD (-1)")
#     return OffsetCoord(col, row)
#
#
# def r_offset_to_cube(offset, h):
#     q = h.col - (h.row + offset * (h.row & 1)) // 2
#     r = h.row
#     s = -q - r
#     if offset != EVEN and offset != ODD:
#         raise ValueError("offset must be EVEN (+1) or ODD (-1)")
#     return hexagon(q, r, s)
#
#
# DoubledCoord = collections.namedtuple("DoubledCoord", ["col", "row"])
#
#
# def q_doubled_from_cube(h):
#     col = h.q
#     row = 2 * h.r + h.q
#     return DoubledCoord(col, row)
#
#
# def q_doubled_to_cube(h):
#     q = h.col
#     r = (h.row - h.col) // 2
#     s = -q - r
#     return hexagon(q, r, s)
#
#
# def r_doubled_from_cube(h):
#     col = 2 * h.q + h.r
#     row = h.r
#     return DoubledCoord(col, row)
#
#
# def r_doubled_to_cube(h):
#     q = (h.col - h.row) // 2
#     r = h.row
#     s = -q - r
#     return hexagon(q, r, s)
#
#
# Orientation = collections.namedtuple("Orientation", ["f0", "f1", "f2", "f3", "b0", "b1", "b2", "b3", "start_angle"])
#
# Layout = collections.namedtuple("Layout", ["orientation", "size", "origin"])
#
# layout_pointy = Orientation(math.sqrt(3.0), math.sqrt(3.0) / 2.0, 0.0, 3.0 / 2.0, math.sqrt(3.0) / 3.0, -1.0 / 3.0, 0.0,
#                             2.0 / 3.0, 0.5)
# layout_flat = Orientation(3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0), 2.0 / 3.0, 0.0, -1.0 / 3.0,
#                           math.sqrt(3.0) / 3.0, 0.0)
#
#
# # used
# def hexagon_to_pixel(layout, h):
#     m = layout.orientation
#     size = layout.size
#     origin = layout.origin
#     x = (m.f0 * h.q + m.f1 * h.r) * size.x
#     y = (m.f2 * h.q + m.f3 * h.r) * size.y
#     return Point(x + origin.x, y + origin.y)
#
#
# # used
# def pixel_to_hexagon(layout, p):
#     m = layout.orientation
#     size = layout.size
#     origin = layout.origin
#     pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
#     q = m.b0 * pt.x + m.b1 * pt.y
#     r = m.b2 * pt.x + m.b3 * pt.y
#     return hexagon(q, r, -q - r)
#
#
# # used
# def hexagon_corner_offset(layout, corner):
#     m = layout.orientation
#     size = layout.size
#     angle = 2.0 * math.pi * (m.start_angle - corner) / 6.0
#     return Point(size.x * math.cos(angle), size.y * math.sin(angle))
#
#
# # used
# def polygon_corners(layout, h):
#     corners = []
#     center = hexagon_to_pixel(layout, h)
#     for i in range(0, 6):
#         offset = hexagon_corner_offset(layout, i)
#         corners.append(Point(center.x + offset.x, center.y + offset.y))
#     return corners
#
