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
            "Exit"
            ]
        self.selected = 0
        self.option_rects = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            return self.options[i]

        return None

    def draw(self, screen):
        start_x = 220
        self.option_rects = []

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.small_font.render(option, True, color)

            option_rect = option_text.get_rect(
                midtop=(start_x + i * 200, 800)
            )
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)


class MenuOptions:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.options = [
            "Sound",
            "Music",
            "Theme",
            "Back",
        ]
        self.selected = 0
        self.option_rects = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            return self.options[i]

        return None

    def draw(self, screen):
        start_x = 260
        self.option_rects = []

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.font.render(option, True, color)

            option_rect = option_text.get_rect(
                midtop=(start_x + i * 180, 800)
            )
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)


class MenuPause:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.options = [
            "Resume game",
            "Return to main menu",
        ]
        self.selected = 0
        self.option_rects = []

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            return self.options[i]

        return None

    def draw(self, screen):
        start_x = 260
        self.option_rects = []

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.font.render(option, True, color)

            option_rect = option_text.get_rect(
                midtop=(start_x + i * 180, 800)
            )
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)
