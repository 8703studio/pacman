import pygame

from src.interface.menu import GameInterface
from src.interface.screens.highscores_screen import HighscoresScreen


class NameInputScreen:

    """Handles player name input for the high score."""

    def __init__(
        self,
        game: GameInterface,
    ) -> None:

        """Initialize the name input screen."""

        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:

            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(
            theme.background_image
        ).convert()

        self.name = ""

        self.score = 12500

        self.font = pygame.font.Font(None, 50)

        self.title = pygame.font.Font(None, 70)

        self.message_font = pygame.font.Font(None, 32)

        self.input_rect = pygame.Rect(
            0,
            0,
            400,
            70,
        )

        self.continue_button = pygame.Rect(
            0,
            0,
            200,
            60,
        )

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:

        """Handle player name input events."""

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    self._submit_name()

                elif event.key == pygame.K_BACKSPACE:

                    self.name = self.name[:-1]

                else:

                    if len(self.name) < 10 and (
                        event.unicode.isalnum()
                        or event.unicode == " "
                    ):

                        self.name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if self.continue_button.collidepoint(
                        event.pos
                    ):

                        self._submit_name()

    def _submit_name(self) -> None:

        """Submit the player name."""

        name = self.name.strip()

        if not name:

            return

        self.game.change_screen(
            HighscoresScreen(self.game)
        )

    def update(self, delta_time: float) -> None:

        """Update the name input screen."""

        pass

    def draw(self, screen: pygame.Surface) -> None:

        """Draw the name input screen."""

        width = screen.get_width()
        height = screen.get_height()

        self.background = pygame.transform.scale(
            self.background,
            screen.get_size(),
        )

        screen.blit(
            self.background,
            (0, 0),
        )

        theme = self.game.theme_manager.get_theme()

        title = self.title.render(
            "ENTER YOUR NAME",
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(
            center=(
                width // 2,
                int(height * 0.185),
            )
        )

        screen.blit(title, title_rect)

        self.input_rect.center = (
            width // 2,
            int(height * 0.324),
        )

        pygame.draw.rect(
            screen,
            theme.menu_text_color,
            self.input_rect,
            2,
        )

        name_text = self.font.render(
            self.name,
            True,
            theme.menu_text_color,
        )

        name_rect = name_text.get_rect(
            center=self.input_rect.center
        )

        screen.blit(name_text, name_rect)

        message = self.message_font.render(
            "10 characters maximum",
            True,
            theme.menu_text_color,
        )

        message_rect = message.get_rect(
            center=(
                width // 2,
                int(height * 0.417),
            )
        )

        screen.blit(message, message_rect)

        self.continue_button.center = (
            width // 2,
            int(height * 0.463),
        )

        pygame.draw.rect(
            screen,
            theme.title_text_color,
            self.continue_button,
        )

        button_text = self.message_font.render(
            "CONTINUE",
            True,
            theme.menu_text_color,
        )

        button_text_rect = button_text.get_rect(
            center=self.continue_button.center
        )

        screen.blit(button_text, button_text_rect)
