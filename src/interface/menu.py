import pygame
from src.interface import colors


class MenuStartScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.options = [
            "Start Game",
            "View Highscores",
            "Instructions",
            "Options",
            ]
        self.selected = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]

        return None

    def draw(self, screen):
        start_x = 260

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.small_font.render(option, True, color)

            option_rect = option_text.get_rect(
                midtop=(start_x + i * 180, 800)
            )

            screen.blit(option_text, option_rect)


class MenuOptionsScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.title_text = self.font.render("OPTIONS", True, colors.white)

        self.options = [
            "",
            "",
            "",
            "",
            ]
        self.selected = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]

        return None

    def draw(self, screen):
        start_x = 260

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.small_font.render(option, True, color)

            option_rect = option_text.get_rect(
                midtop=(start_x + i * 180, 800)
            )

            screen.blit(option_text, option_rect)
