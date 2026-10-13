import pygame

from src.interface.menu import GameInterface
from src.interface.background import draw_background
from src.interface.screens.name_input_screen import NameInputScreen


class EndGameScreen:
    """Displays the end game screen."""

    def __init__(
        self,
        game: GameInterface,
        victory: bool,
    ) -> None:
        """Initialize the end game screen."""

        self.game = game
        self.victory = victory

        theme = self.game.theme_manager.get_theme()

        self.score = 12500

        self.font = pygame.font.Font(theme.font_path, 48)
        self.title = pygame.font.Font(theme.font_path, 70)
        self.font_message = pygame.font.Font(theme.font_path, 32)

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
        """Handle events from the end game screen."""

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_screen(
                        NameInputScreen(self.game, self.score)
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.continue_button.collidepoint(
                        event.pos
                    ):
                        self.game.change_screen(
                            NameInputScreen(self.game, self.score)
                        )

    def update(self, delta_time: float) -> None:
        """Update the end game screen."""

        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the end game screen."""

        theme = self.game.theme_manager.get_theme()

        draw_background(
            screen,
            theme.background_color,
            None,
            # theme.background_image,
        )

        width = screen.get_width()
        height = screen.get_height()

        if self.victory:
            title_text = "VICTORY!"
        else:
            title_text = "GAME OVER"

        title = self.title.render(
            title_text,
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(
            center=(
                width // 2,
                int(height * 0.278),
            )
        )

        screen.blit(title, title_rect)

        score = self.font.render(
            f"Final score: {self.score}",
            True,
            theme.menu_text_color,
        )

        score_rect = score.get_rect(
            center=(
                width // 2,
                int(height * 0.417),
            )
        )

        screen.blit(score, score_rect)

        self.continue_button.center = (
            width // 2,
            int(height * 0.602),
        )

        pygame.draw.rect(
            screen,
            theme.button_color,
            self.continue_button,
        )

        button_text = self.font_message.render(
            "CONTINUE",
            True,
            theme.button_color_text,
        )

        button_text_rect = button_text.get_rect(
            center=self.continue_button.center
        )

        screen.blit(
            button_text,
            button_text_rect,
        )
