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

        self.background = pygame.image.load(theme.background_image).convert()

        self.background = pygame.transform.scale(self.background, (1024, 1080))

        # self.banner = pygame.image.load(
        #     "pac-idol.png"
        # ).convert_alpha()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 30
        )
        self.highscore_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 32
        )
        self.banner_rect = pygame.Rect(100, 150, 824, 450)
        self.subtitle_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 36
        )
        self.menu = MenuStartScreen(self.game)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the main menu."""
        action = self.menu.handle_events(events)

        if action == "Start Game":
            self.game.change_screen(
                GameScreen(cast(GameScreenInterface, self.game))
                )

        elif action == "View Highscores":
            self.game.change_screen(HighscoresScreen(self.game))

        elif action == "Instructions":
            self.game.change_screen(InstructionsScreen(self.game))

        elif action == "Options":
            self.game.change_screen(OptionsScreen(self.game))

        elif action == "Exit":
            self.game.running = False

    def update(self, delta_time: float) -> None:
        """Update the main menu screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu screen."""
        screen.blit(self.background, (0, 0))
        theme = self.game.theme_manager.get_theme()
        # screen.fill(colors.black)

        highscore = self.highscore_font.render(
            "HIGH SCORE : 12500", True, theme.menu_text_color
        )

        highscore_rect = highscore.get_rect(
            centerx=screen.get_width() // 2, top=30
        )

        screen.blit(highscore, highscore_rect)

        pygame.draw.rect(screen, theme.menu_text_color, self.banner_rect, 3)

        subtitle = self.subtitle_font.render(
            "K-POP ARCADE", True, theme.title_text_color
        )

        subtitle_rect = subtitle.get_rect(
            centerx=screen.get_width() // 2, top=self.banner_rect.bottom + 20
        )

        screen.blit(subtitle, subtitle_rect)

        # banner_rect = self.banner.get_rect()
        # banner_rect.centerx = screen.get_rect().centerx
        # banner_rect.top = 100

        # screen.blit(self.banner, banner_rect)

        self.menu.draw(screen)
