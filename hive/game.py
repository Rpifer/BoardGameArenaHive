from hive import piece, hexutil, board
import pygame
import math


class Game:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self._sys_font = None
        self._background = None
        self._layout = None
        self.board = board.Board()
        self.size = self.width, self.height = 500, 500
        self.origin = hexutil.Point(self.width // 2, self.height // 2)
        self.scale = 50
        self.selected_piece = None

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._sys_font = pygame.font.get_default_font()
        self._background = pygame.Surface(self._display_surface.get_size())
        self._background.fill((219, 210, 127))

        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = pygame.mouse.get_pos()
            closest_piece = None
            min_distance = 10000
            # find closest hexagon that was clicked
            for tile in self.board.get_occupied_tiles():
                p = hexutil.hexagon_to_pixel(self.origin, hexutil.Point(tile.x, tile.y), self.scale)
                if math.sqrt(abs(p.x - clicked[0]) ** 2 + abs(p.y - clicked[1]) ** 2) < min_distance:
                    closest_piece = tile.piece
                    min_distance = math.sqrt(abs(p.x - clicked[0]) ** 2 + abs(p.y - clicked[1]) ** 2)
            if min_distance < self.scale:
                self.selected_piece = closest_piece
                print('Piece Selected')
            else:
                self.selected_piece = None
                print('Piece Unselected')

    def on_loop(self):
        pass

    def on_render(self):
        labels = []
        font = pygame.font.SysFont(None, 48)
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
            pygame.draw.polygon(self._background, ((0, 0, 0), (255, 255, 255))[tile.piece.color == 'B'],
                                hexutil.polygon_corners(self.origin, hexutil.Point(tile.x, tile.y), self.scale),
                                2)
        self._display_surface.blit(self._background, (0, 0))

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
    g.board.add_piece(0, 1, piece.create_beetle('B'))
    g.board.add_piece(-1, 3, piece.create_beetle('W'))
    g.board.add_piece(0, 2, piece.create_mosquito('W'))
    g.board.add_piece(1, 1, piece.create_queen('W'))
    g.board.add_piece(2, 2, piece.create_pill('B'))
    g.board.add_piece(1, 0, piece.create_ladybug('B'))
    g.board.add_piece(2, 0, piece.create_spider('B'))
    g.board.add_piece(3, 0, piece.create_pill('B'))
    g.board.add_piece(2, 1, piece.create_pill('B'))
    g.on_execute()
