import pygame

from src.interface import colors


class HUD:
    def __init__(self, font_size: int = 32) -> None:
        self.font = pygame.font.Font(None, font_size)
        self.color = colors.white

        self.level_icon = pygame.image.load(
            "./src/interface/assets/img/hud/level.png"
        )

        self.score_icon = pygame.image.load(
            "./src/interface/assets/img/hud/score.png"
        )

        self.heart_icon = pygame.image.load(
            "./src/interface/assets/img/hud/heart.png"
        )

        self.clock_icon = pygame.image.load(
            "./src/interface/assets/img/hud/clock.png"
        )

    def render(
        self,
        screen,
        score: int,
        lives: int,
        level: int,
        time_left: int
    ) -> None:
        """Render the HUD on the screen."""

        width = screen.get_width()

        level_text = self.font.render(
            f"Level: {level}",
            True,
            self.color
        )

        level_rect = level_text.get_rect(
            midtop=(width // 2, 10)
        )

        level_icon_rect = self.level_icon.get_rect(
            midright=(level_rect.left - 5, level_rect.centery)
        )

        screen.blit(self.level_icon, level_icon_rect)
        screen.blit(level_text, level_rect)

        top_y = 70

        score_text = self.font.render(
            f"Score: {score}",
            True,
            self.color
        )

        score_rect = score_text.get_rect(
            topleft=(20, top_y)
        )

        score_icon_rect = self.score_icon.get_rect(
            midleft=(score_rect.right + 5, score_rect.centery)
            )

        screen.blit(score_text, score_rect)
        screen.blit(self.score_icon, score_icon_rect)

        lives_text = self.font.render(
            f"Lives: {lives}",
            True,
            self.color
        )

        lives_rect = lives_text.get_rect(
            midtop=(width // 2, top_y)
        )

        lives_icon_rect = self.heart_icon.get_rect(
            midright=(lives_rect.left - 5, lives_rect.centery)
        )

        screen.blit(self.heart_icon, lives_icon_rect)
        screen.blit(lives_text, lives_rect)

        time_text = self.font.render(
            f"Time Left: {time_left}",
            True,
            self.color
        )

        time_rect = time_text.get_rect(
            topright=(width - 20, top_y)
        )

        time_icon_rect = self.clock_icon.get_rect(
            midright=(time_rect.left - 5, time_rect.centery)
        )

        screen.blit(self.clock_icon, time_icon_rect)
        screen.blit(time_text, time_rect)
