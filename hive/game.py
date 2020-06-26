from hive import piece, hexutil, board
import pygame
import math


class Game:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self._sys_font = None
        self._background = None
        self._playSurface = None
        self._layout = None
        self.board = board.Board()
        self.size = self.width, self.height = 500, 500
        self.origin = hexutil.Point(self.width // 2, self.height // 2)
        self.scale = 50
        self.selected_piece = None
        self.drag = False
        self.last_coord = None

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._sys_font = pygame.font.get_default_font()
        self._background = pygame.Surface(self._display_surface.get_size())
        self._background.fill((219, 210, 127))
        self._playSurface = pygame.Surface(self._display_surface.get_size())
        self._playSurface.fill((219, 210, 127))

        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = pygame.mouse.get_pos()

            if event.button == 4:
                self.scale = self.scale + 2
            elif event.button == 5:
                self.scale = self.scale - 2
            elif event.button == 3:
                self.drag = True
                self.last_coord = hexutil.Point(clicked[0], clicked[1])

            elif event.button == 1:
                est = hexutil.pixel_to_closest_hexagon(self.origin, hexutil.Point(clicked[0], clicked[1]), self.scale)
                if est is not None:
                    # todo: figure out z axis here
                    if self.board.space_occupied(est.x, est.y):
                        self.selected_piece = self.board.piece_at(est.x, est.y, 0)
                    else:
                        self.board.add_piece(est.x, est.y, piece.create_spider('B'))
                else:
                    self.selected_piece = None

        if event.type == pygame.MOUSEBUTTONUP:
            self.drag = False
            self.last_coord = None

        if event.type == pygame.MOUSEMOTION:
            if self.drag:
                place = pygame.mouse.get_pos()
                coord = hexutil.Point(place[0], place[1])
                self.origin = hexutil.Point(self.origin.x + (coord.x - self.last_coord.x),
                                            self.origin.y + (coord.y - self.last_coord.y), )
                self.last_coord = coord

    def on_loop(self):
        pass

    def on_render(self):
        labels = []
        font = pygame.font.SysFont(None, 48)
        self._playSurface.fill((219, 210, 127))
        for tile in self.board.get_occupied_tiles():
            text = font.render(tile.piece.species, True, (255, 0, 0))
            if tile.piece is self.selected_piece:
                text = font.render(tile.piece.species, True, (0, 180, 180))

            text_rect = text.get_rect()
            # set the center of the rectangular object.
            text_rect.center = hexutil.hexagon_to_pixel(self.origin,
                                                        hexutil.Point(tile.x, tile.y),
                                                        self.scale)
            labels.append((text, text_rect))
            pygame.draw.polygon(self._playSurface, ((0, 0, 0), (255, 255, 255))[tile.piece.color == 'B'],
                                hexutil.polygon_corners(self.origin, hexutil.Point(tile.x, tile.y), self.scale),
                                2)

        self._display_surface.blit(self._background, (0, 0))
        self._display_surface.blit(self._playSurface, (0, 0))

        for label in labels:
            self._display_surface.blit(label[0], label[1])
        pygame.display.flip()  # flip the screen like in a flipbook

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
    g.board.add_piece(0, 0, piece.create_ant('W'))
    # g.board.add_piece(0, 1, piece.create_beetle('B'))
    # g.board.add_piece(-1, 3, piece.create_beetle('W'))
    # g.board.add_piece(0, 2, piece.create_mosquito('W'))
    # g.board.add_piece(1, 1, piece.create_queen('W'))
    # g.board.add_piece(2, 2, piece.create_pill('B'))
    # g.board.add_piece(1, 0, piece.create_ladybug('B'))
    # g.board.add_piece(2, 0, piece.create_spider('B'))
    # g.board.add_piece(3, 0, piece.create_pill('B'))
    # g.board.add_piece(2, 1, piece.create_pill('B'))
    g.on_execute()
