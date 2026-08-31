import pygame

from src.interface.theme.theme import CLASSIC_THEME
from src.interface.theme.theme_manager import ThemeManager


class GameWindow:
    def __init__(self, width, height):
        pygame.init()

        self.theme_manager = ThemeManager(CLASSIC_THEME)
        self.running = True
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-idol")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass

    def update(self, delta_time):
        pass

    def draw(self):
        pass

    def draw_maze(self, maze):
        pass

    def draw_entities(self, player, ghosts, pellets):
        pass

    def run(self):
        while self.running:
            self.handle_events()
            delta_time = self.clock.tick(60) / 1000
            self.update(delta_time)
            self.draw()
            pygame.display.flip()
