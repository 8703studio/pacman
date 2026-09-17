import pygame

from src.interface.menu import GameInterface
from src.interface.utils import draw_text


class InstructionsScreen:
    """Displays the game instructions."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the instructions screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 26
        )

        self.small_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 24
        )

        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 60
        )

        self.section_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 30
        )

        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 20
        )

        self.back_button = pygame.Rect(100, 950, 100, 55)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the instructions screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.show_start_screen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.game.show_start_screen()

    def update(self, delta_time: float) -> None:
        """Update the instructions screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the instructions screen."""
        screen.blit(self.background, (0, 0))

        theme = self.game.theme_manager.get_theme()

        # Title
        title_text = "HOW TO PLAY"

        title = self.title.render(
            title_text,
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(
            centerx=screen.get_width() // 2,
            top=100,
        )

        screen.blit(title, title_rect)

        # Main instruction panel
        panel_rect = pygame.Rect(
            100,
            180,
            824,
            430,
        )

        pygame.draw.rect(
            screen,
            theme.menu_text_color,
            panel_rect,
            3,
        )

        # Instruction cards
        cards = [
            (
                pygame.Rect(140, 220, 340, 160),
                "MOVE",
                "ARROW KEYS",
            ),
            (
                pygame.Rect(544, 220, 340, 160),
                "PAC-GUM",
                "EAT",
            ),
            (
                pygame.Rect(140, 410, 340, 160),
                "POWER",
                "+50 PTS",
            ),
            (
                pygame.Rect(544, 410, 340, 160),
                "RIVAL IDOLS",
                "AVOID",
            ),
        ]

        for rect, title_text, description in cards:
            pygame.draw.rect(
                screen,
                theme.title_text_color,
                rect,
                2,
            )

            card_title = self.section_font.render(
                title_text,
                True,
                theme.title_text_color,
            )

            card_title_rect = card_title.get_rect(
                centerx=rect.centerx,
                top=rect.top + 15,
            )

            screen.blit(card_title, card_title_rect)

            # Placeholder for future image
            placeholder = pygame.Rect(
                rect.centerx - 25,
                rect.top + 55,
                50,
                50,
            )

            pygame.draw.rect(
                screen,
                theme.menu_text_color,
                placeholder,
                2,
            )

            card_description = self.small_font.render(
                description,
                True,
                theme.menu_text_color,
            )

            description_rect = card_description.get_rect(
                centerx=rect.centerx,
                bottom=rect.bottom - 15,
            )

            screen.blit(
                card_description,
                description_rect,
            )

        # Score system
        draw_text(
            screen,
            "SCORE SYSTEM",
            100,
            650,
            self.section_font,
            theme.title_text_color,
        )

        draw_text(
            screen,
            "PAC-GUM",
            100,
            700,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "10 PTS",
            650,
            700,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "POWER PELLET",
            100,
            735,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "50 PTS",
            650,
            735,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "GHOSTS",
            100,
            770,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "200 PTS",
            650,
            770,
            self.small_font,
            theme.menu_text_color,
        )

        # Lightsticks
        draw_text(
            screen,
            "LIGHTSTICKS",
            100,
            825,
            self.section_font,
            theme.title_text_color,
        )

        lightstick_positions = [
            200,
            300,
            400,
            500,
            600,
            700,
            800,
        ]

        for x in lightstick_positions:
            pygame.draw.rect(
                screen,
                theme.menu_text_color,
                pygame.Rect(
                    x - 20,
                    870,
                    40,
                    55,
                ),
                2,
            )

        # Back button
        pygame.draw.rect(
            screen,
            theme.button_color,
            self.back_button,
        )

        button_text = self.font_button.render(
            "BACK",
            True,
            theme.button_color_text,
        )

        button_text_rect = button_text.get_rect(center=self.back_button.center)

        screen.blit(
            button_text,
            button_text_rect,
        )
