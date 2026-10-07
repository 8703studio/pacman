import pygame

from typing import cast

from src.interface.menu import (
    GameInterface,
    GameScreenInterface,
    MenuStartScreen,
)
from src.interface.screens.game_screen import GameScreen
from src.interface.screens.highscores_screen import HighscoresScreen
from src.interface.screens.instructions_screen import InstructionsScreen
from src.interface.screens.options_screen import OptionsScreen


class StartScreen:
    """Displays the start screen."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the start screen."""

        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background_image = pygame.image.load(
            theme.background_image
        ).convert()

        self.banner_rect = pygame.Rect(
            0,
            0,
            0,
            0,
        )

        self.menu = MenuStartScreen(self.game)

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """Handle events from the main menu."""

        action = self.menu.handle_events(events)

        if action == "Start Game":
            self.game.change_screen(
                GameScreen(cast(GameScreenInterface, self.game))
            )

        elif action == "View Highscores":
            self.game.change_screen(
                HighscoresScreen(self.game)
            )

        elif action == "Instructions":
            self.game.change_screen(
                InstructionsScreen(self.game)
            )

        elif action == "Options":
            self.game.change_screen(
                OptionsScreen(self.game)
            )

        elif action == "Exit":
            self.game.running = False

    def update(self, delta_time: float) -> None:
        """Update the main menu screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu screen."""

        theme = self.game.theme_manager.get_theme()

        screen_size = screen.get_size()

        background = pygame.transform.scale(
            self.background_image,
            screen_size,
        )

        screen.blit(background, (0, 0))

        scale = screen.get_height() / 800

        highscore_size = max(20, int(32 * scale))
        subtitle_size = max(24, int(36 * scale))

        highscore_font = pygame.font.Font(
            theme.font_path,
            highscore_size,
        )

        subtitle_font = pygame.font.Font(
            theme.font_path,
            subtitle_size,
        )

        banner_width = int(screen.get_width() * 0.8)
        banner_height = int(screen.get_height() * 0.42)

        self.banner_rect.size = (
            banner_width,
            banner_height,
        )

        self.banner_rect.centerx = screen.get_width() // 2
        self.banner_rect.top = int(
            screen.get_height() * 0.14
        )

        highscore = highscore_font.render(
            "HIGH SCORE : 12500",
            True,
            theme.menu_text_color,
        )

        highscore_rect = highscore.get_rect(
            centerx=screen.get_width() // 2,
            top=int(30 * scale),
        )

        screen.blit(
            highscore,
            highscore_rect,
        )

        pygame.draw.rect(
            screen,
            theme.menu_text_color,
            self.banner_rect,
            3,
        )

        subtitle = subtitle_font.render(
            "K-POP ARCADE",
            True,
            theme.title_text_color,
        )

        subtitle_rect = subtitle.get_rect(
            centerx=screen.get_width() // 2,
            top=self.banner_rect.bottom + int(20 * scale),
        )

        screen.blit(
            subtitle,
            subtitle_rect,
        )

        self.menu.draw(screen)
