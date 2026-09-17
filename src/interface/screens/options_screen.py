import pygame

from src.interface.menu import GameInterface, MenuOptions


class OptionsScreen:
    """Displays the game options screen."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the options screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(
            theme.background_image
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (1024, 1080)
        )

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
        screen.blit(self.background, (0, 0))

        # screen.fill(colors.black)

        self.menu.draw(screen)
