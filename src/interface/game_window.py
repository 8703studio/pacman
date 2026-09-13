import pygame
from typing import Optional, Any

from src.interface.theme.theme import CLASSIC_THEME
from src.interface.hud import HUD
from src.interface.theme.theme_manager import ThemeManager
from src.interface.maze_renderer import MazeRenderer
from src.interface.screens import StartScreen


class GameWindow:
    """Manages the main game window and its interface screens."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize the game window and its interface components."""
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
            margin=self.margin,
        )

    def handle_events(self) -> None:
        """Handle Pygame events and pass them to the current screen."""
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.current_screen.events(events)

    def update(self, delta_time: float) -> None:
        """Update the current screen."""
        self.current_screen.update(delta_time)

    def change_screen(self, screen: Any) -> None:
        """Change the current interface screen."""
        self.current_screen = screen

    def draw(self) -> None:
        """Draw the current screen on the game window."""
        self.current_screen.draw(self.screen)

    def run(self) -> None:
        """Run the main game loop."""
        while self.running:
            self.handle_events()

            delta_time = self.clock.tick(60) / 1000

            self.update(delta_time)
            self.draw()

            pygame.display.flip()

        pygame.quit()
