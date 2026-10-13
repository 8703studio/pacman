import pygame

from src.interface.menu import GameInterface, MenuOptions
from src.interface.background import draw_background


class OptionsScreen:
    """Displays the game options screen."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the options screen."""

        self.game = game

        self.menu = MenuOptions(self.game)

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """Handle events from the options menu."""

        action = self.menu.handle_events(events)

        for event in events:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_BACKSPACE
            ):
                action = "Back"

        if action == "Back":
            self.game.show_start_screen()

    def update(self, delta_time: float) -> None:
        """Update the options screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the options screen."""

        theme = self.game.theme_manager.get_theme()

        draw_background(
            screen,
            theme.background_color,
            None,
            # theme.background_image,
        )

        self.menu.draw(screen)
