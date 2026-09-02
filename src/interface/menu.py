import pygame
from src.interface import colors


class MenuScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.title_text = self.font.render("PAC-IDOL", True, colors.white)

        self.options = [
            "Start Game",
            "View Highscores",
            "Instructions",
            "Options",
            ]
        self.selected = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.K_RIGHT:
                if event.key == pygame.K_LEFT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RIGHT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]  # signale le choix

        return None  # aucun changement d'état ce tour-ci

    def draw(self, screen):
        width = screen.get_width()

        title_rect = self.title_text.get_rect(midtop=(width // 2, 50))
        screen.blit(self.title_text, title_rect)

        start_y = 800
        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white
            option_text = self.small_font.render(option, True, color)
            option_rect = option_text.get_rect(midtop=(width // 2,
                                                       start_y + i * 50))
            screen.blit(option_text, option_rect)
