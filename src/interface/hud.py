
import pygame
from pathlib import Path

from src.interface.theme.theme import Theme


class HUD:
    """Displays the game's heads-up display."""

    def __init__(self, theme: Theme, font_size: int = 32) -> None:
        """Initialize the HUD and load its icons."""
        self.font = pygame.font.Font(theme.font_path, font_size)
        self.color = theme.hud_text_color

        assets_path = (
            Path(__file__).resolve().parent / "assets" / "hud"
        )

        self.level_icon = self._load_icon(
            assets_path / "level.png"
        )
        self.score_icon = self._load_icon(
            assets_path / "star.png"
        )
        self.heart_icon = self._load_icon(
            assets_path / "koreanheart.png"
        )
        self.clock_icon = self._load_icon(
            assets_path / "clock.png"
        )

    @staticmethod

    @staticmethod
    def _load_icon(path: Path) -> pygame.Surface:
        """Load and resize a HUD icon."""
        image = pygame.image.load(str(path))
        image = image.convert_alpha() if pygame.display.get_surface() else image
        return pygame.transform.smoothscale(image, (40, 40))


    def _draw_item(
        self,
        screen: pygame.Surface,
        icon: pygame.Surface,
        text: str,
        position: tuple[int, int],
        align: str = "topleft",
    ) -> None:
        """Draw an icon and its text."""
        rendered_text = self.font.render(
            text,
            True,
            self.color,
        )

        group_width = (
            icon.get_width()
            + 8
            + rendered_text.get_width()
        )
        group_height = max(
            icon.get_height(),
            rendered_text.get_height(),
        )

        x, y = position

        if align == "center":
            x -= group_width // 2
        elif align == "right":
            x -= group_width

        icon_y = y + (group_height - icon.get_height()) // 2
        text_y = y + (
            group_height - rendered_text.get_height()
        ) // 2

        screen.blit(icon, (x, icon_y))
        screen.blit(
            rendered_text,
            (x + icon.get_width() + 8, text_y),
        )


    def render(
        self,
        screen: pygame.Surface,
        score: int,
        lives: int,
        level: int,
        time_left: int,
    ) -> None:
        """Render the HUD on the screen."""
        width = screen.get_width()
        top_y = 20
        second_y = 70

        self._draw_item(
            screen,
            self.score_icon,
            f"Score: {score}",
            (40, top_y),
        )

        self._draw_item(
            screen,
            self.heart_icon,
            f"Lives: {lives}",
            (width // 2, top_y),
            align="center",
        )

        self._draw_item(
            screen,
            self.clock_icon,
            f"Time: {time_left}",
            (width - 40, top_y),
            align="right",
        )

        self._draw_item(
            screen,
            self.level_icon,
            f"Level: {level}",
            (width // 2, second_y),
            align="center",
        )
