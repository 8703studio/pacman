import pygame

from src.interface.theme.theme import Theme


class HUD:
    """Displays the game's heads-up display."""

    def __init__(self, theme: Theme, font_size: int = 32) -> None:
        """Initialize the HUD and load its icons."""
        self.font = pygame.font.Font(theme.font_path, font_size)
        self.color = theme.hud_text_color

        # self.level_icon = pygame.image.load(
        #     "./src/interface/assets/img/hud/level.png"
        # )
        # self.score_icon = pygame.image.load(
        #     "./src/interface/assets/img/hud/score.png"
        # )
        # self.heart_icon = pygame.image.load(
        #     "./src/interface/assets/img/hud/heart.png"
        # )
        # self.clock_icon = pygame.image.load(
        #     "./src/interface/assets/img/hud/clock.png"
        # )

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

        score_text = self.font.render(
            f"Score: {score}",
            True,
            self.color,
        )
        score_rect = score_text.get_rect(
            topleft=(20, top_y),
        )
        screen.blit(score_text, score_rect)

        level_text = self.font.render(
            f"Level: {level}",
            True,
            self.color,
        )
        level_rect = level_text.get_rect(
            center=(width // 2, top_y + 16),
        )
        screen.blit(level_text, level_rect)

        lives_text = self.font.render(
            f"Lives: {lives}",
            True,
            self.color,
        )
        lives_rect = lives_text.get_rect(
            midtop=(width * 3 // 4, top_y),
        )
        screen.blit(lives_text, lives_rect)

        time_text = self.font.render(
            f"Time: {time_left}",
            True,
            self.color,
        )
        time_rect = time_text.get_rect(
            topright=(width - 20, top_y),
        )
        screen.blit(time_text, time_rect)
