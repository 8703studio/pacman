import pygame
import time

from src.interface.menu import MenuStartScreen, MenuOptions
from src.interface import colors


class StartScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        # self.banner = pygame.image.load(
        #     "pac-idol.png"
        # ).convert_alpha()

        self.menu = MenuStartScreen()

    def events(self, events):
        action = self.menu.handle_events(events)

        if action == "Start Game":
            self.game.change_screen(LoadScreen())

        elif action == "View Highscores":
            self.game.change_screen(HighscoresScreen())

        elif action == "Instructions":
            self.game.change_screen(InstructionsScreen())

        elif action == "Options":
            self.game.change_screen(OptionsScreen(self.game))

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        # banner_rect = self.banner.get_rect()
        # banner_rect.centerx = screen.get_rect().centerx
        # banner_rect.top = 100

        # screen.blit(self.banner, banner_rect)

        self.menu.draw(screen)


class LoadScreen:
    def __init__(self, min_duration=1.0):
        self.background = pygame.image.load(
            "background-start.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background, (1024, 1080)
        )

        self.loading_bar = pygame.image.load(
            "loading.png"
        ).convert_alpha()

        self.min_duration = min_duration
        self.start_time = time.time()

    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def is_finished(self):
        return time.time() - self.start_time >= self.min_duration

    def draw(self, screen):
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.min_duration, 1.0)

        screen.blit(self.background, (0, 0))

        bar_width = int(
            self.loading_bar.get_width() * progress
        )

        bar_rect = pygame.Rect(
            0,
            0,
            bar_width,
            self.loading_bar.get_height()
        )

        loading_bar_pos = (
            screen.get_width() // 2
            - self.loading_bar.get_width() // 2,
            500
        )

        screen.blit(
            self.loading_bar,
            loading_bar_pos,
            area=bar_rect
        )


class OptionsScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.menu = MenuOptions()

    def events(self, events):
        action = self.menu.handle_events(events)

        if action == "Back":
            self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)
        self.menu.draw(screen)


class InstructionsScreen:
    def __init__(self, game):
        self.game = game

        # self.background = pygame.image.load(
        #     "background-instructions.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events):
        action = self.menu.handle_events(events)

        if action == "Back":
            self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time):
        pass

    def draw(self, screen):
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)
        self.menu.draw(screen)


class PauseScreen:
    def __init__(self):
        # self.background = pygame.image.load(
        #     "background-pause.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        pass

    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))


class HighscoresScreen:
    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pass


class GameOverScreen:
    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pass


class VictoryScreen:
    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pass


class NameInputScreen:
    def events(self, events):
        pass

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pass
