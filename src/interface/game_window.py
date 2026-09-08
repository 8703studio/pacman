import pygame
from typing import Optional

from src.interface.theme.theme import CLASSIC_THEME
from src.interface.hud import HUD
from src.interface.theme.theme_manager import ThemeManager
from src.interface.maze_renderer import MazeRenderer
from src.interface.screens import StartScreen


class GameWindow:
    def __init__(self, width, height):
        pygame.init()

        self.theme_manager = ThemeManager(CLASSIC_THEME)

        self.running = True
        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()

        self.hud = HUD()
        self.maze: Optional[list[list[int]]] = None

        self.hud_height = 130
        self.margin = 5

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-idol")

        self.current_screen = StartScreen(self)

        self.maze_renderer = MazeRenderer(
            width=self.width,
            height=self.height,
            hud_height=self.hud_height,
            margin=self.margin
        )

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.current_screen.events(events)

    def update(self, delta_time):
        self.current_screen.update(delta_time)

    def change_screen(self, screen):
        self.current_screen = screen

    def draw(self):
        self.current_screen.draw(self.screen)

    def run(self):
        while self.running:
            self.handle_events()

            delta_time = self.clock.tick(60) / 1000

            self.update(delta_time)
            self.draw()

            pygame.display.flip()

        pygame.quit()
