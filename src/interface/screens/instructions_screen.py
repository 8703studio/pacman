import pygame
from pathlib import Path

from src.interface.menu import GameInterface
from src.interface.utils import draw_text
from src.interface.background import draw_background


class InstructionsScreen:
    """Displays the game instructions."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the instructions screen."""

        self.game = game

        theme = self.game.theme_manager.get_theme()

        self.small_font = pygame.font.Font(
            theme.font_path,
            24,
        )
        self.title = pygame.font.Font(
            theme.font_path,
            70,
        )
        self.section_font = pygame.font.Font(
            theme.font_path,
            30,
        )
        self.font_button = pygame.font.Font(
            theme.font_path,
            20,
        )

        self.back_button = pygame.Rect(0, 0, 100, 60)

        self.assets_path = (
            Path(__file__).resolve().parent.parent / "assets"
        )

        self.instruction_images = {
            "pacgum": pygame.image.load(
                str(
                    self.assets_path
                    / "game"
                    / "hearrtspacgum.png"
                )
            ).convert_alpha(),
            "power": pygame.image.load(
                str(
                    self.assets_path
                    / "game"
                    / "superpacgum.png"
                )
            ).convert_alpha(),
            "ghosts": pygame.image.load(
                str(self.assets_path / "allghosts.png")
            ).convert_alpha(),
        }

        lightstick_dir = self.assets_path / "lighstick"
        lightstick_names = [
            "2NE1-1.png",
            "bm-1.png",
            "bp-1.png",
            "dreamcatcher-1.png",
            "gg-1.png",
            "lesserafim-1.png",
            "mamamoo-1.png",
            "newjeans-1.png",
            "seventeen-1.png",
            "shinee-1.png",
            "vixx-1.png",
        ]

        self.lightsticks = [
            pygame.image.load(
                str(lightstick_dir / name)
            ).convert_alpha()
            for name in lightstick_names
        ]

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

        draw_background(
            screen,
            theme.background_color,
            None,
        )

        title_top = int(height * 0.08)

        title_surface = self.title.render(
            "HOW TO PLAY",
            True,
            theme.menu_text_color,
        )

        title_rect = title_surface.get_rect(
            centerx=center_x,
            top=title_top,
        )

        screen.blit(title_surface, title_rect)

        panel_width = int(width * 0.80)
        panel_height = int(height * 0.39)

        panel_rect = pygame.Rect(
            0,
            0,
            panel_width,
            panel_height,
        )
        panel_rect.centerx = center_x
        panel_rect.top = int(height * 0.15)

        card_width = int(panel_rect.width * 0.415)
        card_height = int(panel_rect.height * 0.37)
        vertical_gap = int(panel_rect.height * 0.07)

        left_x = panel_rect.left + 25
        right_x = panel_rect.right - 25 - card_width
        top_y = panel_rect.top + 25
        bottom_y = top_y + card_height + vertical_gap

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
                None,
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
                self.instruction_images["pacgum"],
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
                self.instruction_images["power"],
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
                self.instruction_images["ghosts"],
            ),
        ]

        for rect, title_text, description, image in cards:
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
                top=rect.top + 6,
            )
            screen.blit(card_title, card_title_rect)

            if image is not None:
                max_width = int(rect.width * 0.75)
                max_height = int(rect.height * 0.48)

                image_ratio = (
                    image.get_width() / image.get_height()
                )

                image_width = min(
                    max_width,
                    int(max_height * image_ratio),
                )
                image_height = int(image_width / image_ratio)

                scaled_image = pygame.transform.smoothscale(
                    image,
                    (image_width, image_height),
                )
                image_rect = scaled_image.get_rect(
                    center=(rect.centerx, rect.centery + 2)
                )
                screen.blit(scaled_image, image_rect)
            else:
                arrows = self.section_font.render(
                    "↑ ↓ ← →",
                    True,
                    theme.menu_text_color,
                )
                arrows_rect = arrows.get_rect(
                    center=(rect.centerx, rect.centery + 2)
                )
                screen.blit(arrows, arrows_rect)

            card_description = self.small_font.render(
                description,
                True,
                theme.menu_text_color,
            )
            description_rect = card_description.get_rect(
                centerx=rect.centerx,
                bottom=rect.bottom - 4,
            )
            screen.blit(card_description, description_rect)

        score_left = int(width * 0.12)
        score_right = int(width * 0.62)
        score_top = int(height * 0.530)
        score_line_gap = int(height * 0.037)

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
            score_top + score_line_gap,
            self.small_font,
            theme.menu_text_color,
        )
        draw_text(
            screen,
            "10 PTS",
            score_right,
            score_top + score_line_gap,
            self.small_font,
            theme.menu_text_color,
        )
        draw_text(
            screen,
            "POWER PELLET",
            score_left,
            score_top + score_line_gap * 2,
            self.small_font,
            theme.menu_text_color,
        )
        draw_text(
            screen,
            "50 PTS",
            score_right,
            score_top + score_line_gap * 2,
            self.small_font,
            theme.menu_text_color,
        )
        draw_text(
            screen,
            "GHOSTS",
            score_left,
            score_top + score_line_gap * 3,
            self.small_font,
            theme.menu_text_color,
        )
        draw_text(
            screen,
            "200 PTS",
            score_right,
            score_top + score_line_gap * 3,
            self.small_font,
            theme.menu_text_color,
        )

        lightstick_title = self.section_font.render(
            "LIGHTSTICKS",
            True,
            theme.title_text_color,
        )
        lightstick_title_rect = lightstick_title.get_rect(
            centerx=center_x,
            top=int(height * 0.690),
        )
        screen.blit(lightstick_title, lightstick_title_rect)

        lightstick_y = int(height * 0.755)
        lightstick_width = min(36, int(width * 0.04))
        lightstick_height = min(42, int(height * 0.06))
        spacing = width / (len(self.lightsticks) + 1)

        for index, lightstick in enumerate(self.lightsticks):
            scaled_lightstick = pygame.transform.smoothscale(
                lightstick,
                (lightstick_width, lightstick_height),
            )
            lightstick_rect = scaled_lightstick.get_rect(
                centerx=int(spacing * (index + 1)),
                top=lightstick_y,
            )
            screen.blit(scaled_lightstick, lightstick_rect)

        self.back_button.bottomleft = (
            int(width * 0.08),
            height - int(height * 0.08),
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
        screen.blit(button_text, button_text_rect)
