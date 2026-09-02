import pygame


class StartScreen:
    def __init__(self):
        self.background = pygame.image.load("background-start.png").convert()
        self.background = pygame.transform.scale(self.background, (1024, 1080))
        self.banner = pygame.image.load("pac-idol.png").convert_alpha()

    def events(self, events):
        pass

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        banner_rect = self.banner.get_rect()
        banner_rect.centerx = screen.get_rect().centerx
        banner_rect.top = 100

        screen.blit(self.banner, banner_rect)


class LoadScreem:
    pass


class OptionsScreen:
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
