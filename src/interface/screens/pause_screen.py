import pygame

from src.interface.menu import GameInterface, MenuPause
from src.interface.screens.start_screen import StartScreen


class PauseScreen:
    """Displays the pause menu."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the pause screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        self.menu = MenuPause(self.game)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the pause menu."""
        action = self.menu.handle_events(events)

        if action == "Resume":
            pass

        elif action == "Return to main menu":
            self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the pause screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pause screen."""
        # screen.fill(colors.black)

        screen.blit(self.background, (0, 0))

        self.menu.draw(screen)
