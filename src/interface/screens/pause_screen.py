import pygame

from src.interface.menu import GameInterface, MenuPause
from src.interface.background import draw_background


class PauseScreen:
    """Displays the pause menu."""

    def __init__(
        self,
        game: GameInterface,
        previous_screen: object,
    ) -> None:
        """Initialize the pause screen."""

        self.game = game
        self.previous_screen = previous_screen

        theme = self.game.theme_manager.get_theme()

        self.font = pygame.font.Font(theme.font_path, 32)
        self.title = pygame.font.Font(theme.font_path, 60)

        self.menu = MenuPause(self.game)

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """Handle events from the pause menu."""

        action = self.menu.handle_events(events)

        if action == "Resume":
            self.game.change_screen(self.previous_screen)

        elif action == "Return to main menu":
            from src.interface.screens.start_screen import StartScreen

            self.game.change_screen(
                StartScreen(self.game)
            )

    def update(self, delta_time: float) -> None:
        """Update the pause screen."""

        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pause screen."""

        theme = self.game.theme_manager.get_theme()

        draw_background(
            screen,
            theme.background_color,
            None,
            # theme.background_image,
        )

        self.menu.draw(screen)
