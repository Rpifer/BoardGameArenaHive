from hive import piece, hexutil, board
import pygame
import math


class Game:
    _display_surface: pygame.Surface
    _board_surface: pygame.Surface
    _player_surface: pygame.Surface

    def __init__(self):
        self._running = True
        self._display_surface = None
        self._sys_font = None
        self._background = None
        self._board_surface = None
        self.board_x_split_percentage = 0.8
        self._player_surface = None
        self.board = board.Board()
        self.size = self.width, self.height = 900, 600
        self.origin = hexutil.Point(self.width // 2, self.height // 2)
        self.scale = 50
        self.selected_piece = None
        self.drag = False
        self.last_coord = None
        self.player_piece_layout = dict(
            W={'Q': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(1)),
               'A': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(2)),
               'S': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(3)),
               'H': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(4)),
               'B': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(5)),
               'M': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(6)),
               'L': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(7)),
               'P': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(8))},
            B={
                'Q': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(9)),
                'A': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(10)),
                'S': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(11)),
                'H': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(12)),
                'B': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(13)),
                'M': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(14)),
                'L': hexutil.Point(self.player_piece_offset(1), self.player_piece_offset(15)),
                'P': hexutil.Point(self.player_piece_offset(1) * 3, self.player_piece_offset(16))})
        self.species_color_map = {
            "A": (17, 99, 207),
            "B": (182, 20, 196),
            "H": (45, 153, 41),
            "L": (179, 13, 7),
            "M": (156, 156, 156),
            "P": (86, 219, 184),
            "Q": (227, 219, 59),
            "S": (115, 85, 46),
        }

    def player_piece_offset(self, num):
        return int(self.height * num / 17) + 1

    def convert_to_play_area_coordinates(self, x, y):
        return x - self.width + int(self.width * self.board_x_split_percentage), y

    def convert_from_play_area_coordinates(self, x, y):
        return x + self.width - int(self.width * self.board_x_split_percentage), y

    def font(self):
        return pygame.font.SysFont("comicsansms", self.scale)

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._sys_font = pygame.font.get_default_font()
        self._background = pygame.Surface(self._display_surface.get_size())
        self._background.fill((219, 210, 127))
        self._board_surface = pygame.Surface((int(self.width * self.board_x_split_percentage), self.height))
        self.origin = hexutil.Point(self.width * self.board_x_split_percentage // 2, self.height // 2)
        self._board_surface.fill((219, 210, 127))
        self._player_surface = pygame.Surface((self.width - int(self.width * self.board_x_split_percentage),
                                               self.height))
        self._player_surface.fill((200, 200, 200))
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = pygame.mouse.get_pos()
            clicked = self.convert_to_play_area_coordinates(clicked[0], clicked[1])
            if clicked[0] > 0 and clicked[1] > 0:
                self.on_play_area_click(event)
            else:
                print(piece)
                # run player click

        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag = False
            self.last_coord = None

        elif event.type == pygame.MOUSEMOTION:
            if self.drag:
                place = pygame.mouse.get_pos()
                coord = hexutil.Point(place[0], place[1])
                # don't need to convert so it can technically move offscreen correctly
                self.origin = hexutil.Point(self.origin.x + (coord.x - self.last_coord.x),
                                            self.origin.y + (coord.y - self.last_coord.y), )
                self.last_coord = coord

    def on_player_area_click(self, event):
        clicked = pygame.mouse.get_pos()
        clicked = self.convert_to_play_area_coordinates(clicked[0], clicked[1])

        if event.button == 4:
            return
        elif event.button == 5:
            return
        elif event.button == 3:
            return
        elif event.button == 1:
            return

    def on_play_area_click(self, event):
        clicked = pygame.mouse.get_pos()
        clicked = self.convert_to_play_area_coordinates(clicked[0], clicked[1])

        if event.button == 4:
            # prevents getting trapped at small scales
            self.scale = int(self.scale * 1.15) + 1
            return
        elif event.button == 5:
            self.scale = max(int(self.scale * .85), 2)
            return
        elif event.button == 3:
            self.drag = True
            self.last_coord = hexutil.Point(clicked[0], clicked[1])
            return

        elif event.button == 1:
            est = hexutil.pixel_to_closest_hexagon(self.origin,
                                                   hexutil.Point(clicked[0], clicked[1]),
                                                   self.scale)
            if est is not None:
                # todo: figure out z axis here
                if self.board.space_occupied(est.x, est.y):
                    if self.selected_piece is not None:
                        self.selected_piece = None
                        return
                    z = 0
                    while self.board.space_occupied(est.x, est.y, z) and z < 7:
                        z = z + 1
                    self.selected_piece = self.board.piece_at(est.x, est.y, z - 1)

                else:
                    self.selected_piece = None
                    return

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surface.blit(self._background, (0, 0))
        self.render_board_space()
        self.render_player_space()

        pygame.display.flip()  # flip the screen like in a flipbook

    def render_player_space(self):
        line_start = self.convert_to_play_area_coordinates(0, self.height)
        pygame.draw.line(self._player_surface, (100, 100, 100), (line_start[0] - 1, 0), (line_start[0] - 1, self.height))
        font = pygame.font.SysFont(None, 36)
        labels = []
        tile: piece.Piece
        last_tile: piece.Piece = piece.Piece("", "")
        offset = 0
        for tile in self.board.player_1.piece_reserve + self.board.player_2.piece_reserve:

            if tile.color == last_tile.color and tile.species == last_tile.species:
                offset += 5
                labels.pop()
            else:
                offset = 0
            text = font.render(tile.species, True, (255, 0, 0))
            text_rect = text.get_rect()
            center = hexutil.hexagon_to_pixel(self.player_piece_layout[tile.color][tile.species],
                                              hexutil.Point(0, 0),
                                              self.player_piece_offset(1) * .9)
            text_rect.center = (center.x + offset, center.y + offset)
            labels.append((text, text_rect))
            corners = hexutil.polygon_corners(self.player_piece_layout[tile.color][tile.species],
                                              hexutil.Point(0, 0), self.player_piece_offset(1) * .9)
            corners = [hexutil.Point(i.x + offset, i.y + offset) for i in corners]
            pygame.draw.polygon(self._player_surface,
                                ((50, 50, 50), (255, 254, 242))[tile.color == 'W'],
                                corners,
                                0)
            pygame.draw.polygon(self._player_surface, (0, 0, 0), corners, 2)
            last_tile = tile

        self._display_surface.blit(self._player_surface, (0, 0))
        for label in labels:
            self._display_surface.blit(label[0], label[1])

    def render_board_space(self):
        self._board_surface.fill((219, 210, 127))
        for tile in self.board.get_occupied_tiles():
            self.render_piece_in_play(self._board_surface, tile, self.scale)

        self._display_surface.blit(self._board_surface,
                                   self.convert_from_play_area_coordinates(0, 0))

    def render_piece_in_play(self, surface, tile, scale):
        font = self.font()
        text = font.render(tile.piece.species, True, self.species_color_map[tile.piece.species])
        offset = 0
        if tile.z > 0:
            offset = 5 * tile.z
        text_rect: pygame.rect = text.get_rect()
        # set the center of the rectangular object.
        center = hexutil.hexagon_to_pixel(self.origin,
                                          hexutil.Point(tile.x, tile.y),
                                          scale)
        text_rect.center = (center.x + offset, center.y + offset)

        corners = hexutil.polygon_corners(self.origin, hexutil.Point(tile.x, tile.y), scale)
        corners = [hexutil.Point(i.x + offset, i.y + offset) for i in corners]
        pygame.draw.polygon(surface,
                            ((50, 50, 50), (222, 220, 193))[tile.piece.color == 'W'],
                            corners,
                            0)
        if tile.piece is self.selected_piece:
            pygame.draw.polygon(surface, (55, 250, 250), corners, scale // 8)
        else:
            pygame.draw.polygon(surface, ((90, 90, 90), (235, 233, 209))[tile.piece.color == 'W'], corners, scale // 12)
        surface.blit(text, text_rect)

    def on_cleanup(self):
        self._running = False
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False
        clock = pygame.time.Clock()
        fps = 30
        while self._running:
            milliseconds = clock.tick(fps)
            for event in pygame.event.get():
                self.on_event(event)
                self.on_loop()
                self.on_render()
        self.on_cleanup()


if __name__ == '__main__':
    g = Game()
    g.board = board.new_default_board()
    g.board.add_piece(0, 0, piece.create_hopper('W'))
    g.on_execute()
