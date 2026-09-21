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

        self.background = pygame.image.load(
            theme.background_image
        ).convert()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            26,
        )

        self.small_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            24,
        )

        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            60,
        )

        self.section_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            30,
        )

        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            20,
        )

        self.back_button = pygame.Rect(
            0,
            0,
            100,
            60,
        )

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
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
        theme = self.game.theme_manager.get_theme()

        width = screen.get_width()
        height = screen.get_height()
        center_x = width // 2

        self.background = pygame.transform.scale(
            self.background,
            screen.get_size(),
        )

        screen.blit(
            self.background,
            (0, 0),
        )

        # Title
        title = self.title.render(
            "HOW TO PLAY",
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(
            centerx=center_x,
            top=int(height * 0.09),
        )

        screen.blit(title, title_rect)

        # Main instruction panel
        panel_width = int(width * 0.80)
        panel_height = int(height * 0.40)

        panel_rect = pygame.Rect(
            0,
            0,
            panel_width,
            panel_height,
        )

        panel_rect.centerx = center_x
        panel_rect.top = int(height * 0.17)

        pygame.draw.rect(
            screen,
            theme.menu_text_color,
            panel_rect,
            3,
        )

        # Instruction cards
        card_width = int(panel_rect.width * 0.415)
        card_height = int(panel_rect.height * 0.37)

        vertical_gap = int(panel_rect.height * 0.07)

        left_x = panel_rect.left + 40

        right_x = (
            panel_rect.right
            - 40
            - card_width
        )

        top_y = panel_rect.top + 40

        bottom_y = (
            top_y
            + card_height
            + vertical_gap
        )

        cards = [
            (
                pygame.Rect(
                    left_x,
                    top_y,
                    card_width,
                    card_height,
                ),
                "MOVE",
                "ARROW KEYS",
            ),
            (
                pygame.Rect(
                    right_x,
                    top_y,
                    card_width,
                    card_height,
                ),
                "PAC-GUM",
                "EAT",
            ),
            (
                pygame.Rect(
                    left_x,
                    bottom_y,
                    card_width,
                    card_height,
                ),
                "POWER",
                "+50 PTS",
            ),
            (
                pygame.Rect(
                    right_x,
                    bottom_y,
                    card_width,
                    card_height,
                ),
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

            screen.blit(
                card_title,
                card_title_rect,
            )

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
        score_left = int(width * 0.10)
        score_right = int(width * 0.635)
        score_top = int(height * 0.60)

        draw_text(
            screen,
            "SCORE SYSTEM",
            score_left,
            score_top,
            self.section_font,
            theme.title_text_color,
        )

        draw_text(
            screen,
            "PAC-GUM",
            score_left,
            score_top + int(height * 0.046),
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "10 PTS",
            score_right,
            score_top + int(height * 0.046),
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "POWER PELLET",
            score_left,
            score_top + int(height * 0.079),
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "50 PTS",
            score_right,
            score_top + int(height * 0.079),
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "GHOSTS",
            score_left,
            score_top + int(height * 0.111),
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "200 PTS",
            score_right,
            score_top + int(height * 0.111),
            self.small_font,
            theme.menu_text_color,
        )

        # Lightsticks
        lightstick_title_y = int(height * 0.764)

        draw_text(
            screen,
            "LIGHTSTICKS",
            score_left,
            lightstick_title_y,
            self.section_font,
            theme.title_text_color,
        )

        lightstick_y = int(height * 0.806)

        lightstick_positions = [
            int(width * 0.195),
            int(width * 0.293),
            int(width * 0.391),
            int(width * 0.488),
            int(width * 0.586),
            int(width * 0.684),
            int(width * 0.781),
        ]

        for x in lightstick_positions:
            pygame.draw.rect(
                screen,
                theme.menu_text_color,
                pygame.Rect(
                    x - 20,
                    lightstick_y,
                    40,
                    55,
                ),
                2,
            )

        # Back button
        self.back_button.bottomleft = (
            100,
            height - 80,
        )

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

        button_text_rect = button_text.get_rect(
            center=self.back_button.center,
        )

        screen.blit(
            button_text,
            button_text_rect,
        )
