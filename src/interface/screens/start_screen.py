
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

from src.interface.background import draw_background


class StartScreen:
    """Displays the start screen."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the start screen."""

        self.game = game

        self.banner_rect = pygame.Rect(0, 0, 0, 0)

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

    def draw_maze(self, screen: pygame.Surface, scale: float) -> None:
        """Draw a neon pixel maze around the edges of the title screen."""
        width, height = screen.get_size()

        theme = self.game.theme_manager.get_theme()

        color1 = theme.accent_color
        color2 = theme.menu_selected_color

        wall = max(4, int(6 * scale))
        unit = max(18, int(28 * scale))
        margin = int(24 * scale)

        paths = [
            # Top-left
            (color1, [
                (margin, int(130 * scale)),
                (margin, margin),
                (int(width * 0.28), margin),
                (int(width * 0.28), int(65 * scale)),
            ]),
            (color2, [
                (int(65 * scale), int(150 * scale)),
                (int(65 * scale), int(65 * scale)),
                (int(width * 0.20), int(65 * scale)),
            ]),
            # Top-right
            (color2, [
                (int(width * 0.72), margin),
                (width - margin, margin),
                (width - margin, int(130 * scale)),
            ]),
            (color1, [
                (int(width * 0.80), int(65 * scale)),
                (width - int(65 * scale), int(65 * scale)),
                (width - int(65 * scale), int(150 * scale)),
            ]),
            # Bottom-left
            (color2, [
                (margin, int(height * 0.72)),
                (margin, height - margin),
                (int(width * 0.28), height - margin),
            ]),
            (color1, [
                (int(65 * scale), int(height * 0.80)),
                (int(65 * scale), height - int(65 * scale)),
                (int(width * 0.20), height - int(65 * scale)),
            ]),
            # Bottom-right
            (color1, [
                (int(width * 0.72), height - margin),
                (width - margin, height - margin),
                (width - margin, int(height * 0.72)),
            ]),
            (color2, [
                (int(width * 0.80), height - int(65 * scale)),
                (width - int(65 * scale), height - int(65 * scale)),
                (width - int(65 * scale), int(height * 0.80)),
            ]),
        ]

        for color, points in paths:
            pygame.draw.lines(screen, color, False, points, wall)

        # Small pixel-like blocks at the ends of some paths.
        for x, y, color in [
            (int(width * 0.34), margin, color1),
            (int(width * 0.66), margin, color2),
            (int(width * 0.34), height - margin, color2),
            (int(width * 0.66), height - margin, color1),
        ]:
            pygame.draw.rect(
                screen,
                color,
                (x, y, unit, wall),
            )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu screen."""

        theme = self.game.theme_manager.get_theme()

        draw_background(
            screen,
            theme.background_color,
            None,
        )

        # Scale everything according to the screen height.
        scale = screen.get_height() / 800

        # Draw the neon maze around the edges.
        self.draw_maze(screen, scale)

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

        # Position the title area.
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

        # Display the best score.
        top_scores = self.game.highscore.top_score(1)
        best_score = top_scores[0]["score"] if top_scores else 0

        highscore = highscore_font.render(
            f"HIGH SCORE : {best_score}",
            True,
            theme.menu_text_color,
        )

        highscore_rect = highscore.get_rect(
            centerx=screen.get_width() // 2,
            top=int(120 * scale),
        )

        screen.blit(highscore, highscore_rect)

        # Display START without the rectangular banner outline.
        start_text = subtitle_font.render(
            "START",
            True,
            theme.title_text_color,
        )

        start_rect = start_text.get_rect(
            centerx=screen.get_width() // 2,
            top=self.banner_rect.bottom + int(20 * scale),
        )

        self.menu.start_button_rect = start_rect

        screen.blit(start_text, start_rect)

        self.menu.draw(screen)