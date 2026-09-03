import pygame
import time
from src.interface.menu import MenuStartScreen
from src.interface import colors


class StartScreen:
    def __init__(self):
        self.background = pygame.image.load("background-start.png").convert()
        self.background = pygame.transform.scale(self.background, (1024, 1080))
        self.banner = pygame.image.load("pac-idol.png").convert_alpha()
        self.menu = MenuStartScreen()

    def events(self, events):
        return self.menu.handle_events(events)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        banner_rect = self.banner.get_rect()
        banner_rect.centerx = screen.get_rect().centerx
        banner_rect.top = 100

        screen.blit(self.banner, banner_rect)
        self.menu.draw(screen)

        self.title_text = self.font.render("", True, colors.white)


class LoadScreen:
    def __init__(self, min_duration=1.0):
        self.background = pygame.image.load("background-start.png").convert()
        self.background = pygame.transform.scale(self.background, (1024, 1080))
        self.loading_bar = pygame.image.load("loading.png").convert_alpha()
        self.min_duration = min_duration
        self.start_time = time.time()

    def events(self, events):
        pass

    def is_finished(self):
        return time.time() - self.start_time >= self.min_duration

    def draw(self, screen):
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.min_duration, 1.0)

        screen.blit(self.background, (0, 0))

        bar_width = int(self.loading_bar.get_width() * progress)
        bar_rect = pygame.Rect(0, 0, bar_width, self.loading_bar.get_height())
        loading_bar_pos = (screen.get_width() // 2 -
                           self.loading_bar.get_width() // 2, 500)

        screen.blit(self.loading_bar, loading_bar_pos, area=bar_rect)


class OptionsScreen:
    def __init__(self, screen):
        self.background = pygame.image.load("background-start.png").convert()
        self.background = pygame.transform.scale(self.background, (1024, 1080))

    def events(self, events):
        pass

    def draw(self, screen):
        pass


class InstructionsScreen:
    def draw(self, screen):
        pass


class PauseScreen:
    def draw(self, screen):
        pass


class HighscoresScreen:
    def draw(self, screen):
        pass


class GameOverScreen:
    def draw(self, screen, final_score):
        pass


class VictoryScreen:
    def draw(self, screen, final_score):
        pass


class NameInputScreen:
    def handle_key(self, key, current_text):
        pass

    def draw(self, screen, current_text):
        pass
