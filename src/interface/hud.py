import pygame
from interface import colors

class HUD:
    def __init__(self, font_size: int = 32) -> None:
        self.font = pygame.font.Font(None, font_size)
        self.color = colors.white

    def render(self, screen, score: int, lives: int, level: int, time_left: int) -> None:
        '''Render the HUD on the screen.'''
        score_text = self.font.render(f"Score: {score}", True, self.color)
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)

        lives_text = self.font.render(f"Lives: {lives}", True, self.color)
        lives_rect = lives_text.get_rect(midtop=(screen.get_width() // 2, 50))
        screen.blit(lives_text, lives_rect)

        level_text = self.font.render(f"Level: {level}", True, self.color)
        level_rect = level_text.get_rect(topright=(screen.get_width() - 10, 10))
        screen.blit(level_text, level_rect)

        time_text = self.font.render(f"Time Left: {time_left}", True, self.color)
        time_rect = time_text.get_rect(topright=(screen.get_width() - 10, 50))
        screen.blit(time_text, time_rect)
