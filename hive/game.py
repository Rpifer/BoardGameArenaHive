from hive import piece, hexutil, board
import pygame


class Game:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self._sys_font = None
        self._background = None
        self._layout = None
        self.board = board.Board()
        self.size = self.width, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._sys_font = pygame.font.get_default_font()
        self._background = pygame.Surface(self._display_surface.get_size())
        self._background.fill((255, 255, 255))
        self._layout = hexutil.Layout(hexutil.layout_flat, hexutil.Point(40, 40),
                                      hexutil.Point(self.width // 2, self.height // 2))
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        min_x, max_x, min_y, max_y = 0
        bounds = self.board.get_bounding_limits()
        pass

    def on_render(self):
        labels = []
        font = pygame.font.SysFont(None, 48)
        for h in self.board.play_space.items():
            text = font.render(h[1].piece.species, True, (255, 0, 0))
            text_rect = text.get_rect()
            # set the center of the rectangular object.
            text_rect.center = hexutil.hexagon_to_pixel(self._layout, h[1].tile)
            labels.append((text, text_rect))
            pygame.draw.polygon(self._background, (50, 50, 50),
                                hexutil.polygon_corners(self._layout, h[1].tile), (2, 0)[h[1].piece.color == 'B'])
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
    g.board.add_piece(0, 2, piece.create_mosquito('W'))
    g.board.add_piece(0, 3, piece.create_queen('W'))
    g.board.add_piece(1, 0, piece.create_pill('B'))
    g.on_execute()
