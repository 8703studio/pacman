import pygame

from src.interface.screens import StartScreen
from src.interface.theme.theme import CLASSIC_THEME
from src.interface.theme.theme_manager import ThemeManager


class TestGame:

    def __init__(self):
        self.running = True
        self.theme_manager = ThemeManager(CLASSIC_THEME)

    def change_screen(self, screen):
        self.current_screen = screen


pygame.init()

screen = pygame.display.set_mode((1024, 1080))
pygame.display.set_caption("Test Start Screen")

game = TestGame()
game.current_screen = StartScreen(game)

clock = pygame.time.Clock()
running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            game.running = False

    game.current_screen.events(events)
    game.current_screen.update(0)

    screen.fill((0, 0, 0))
    game.current_screen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

    running = game.running

pygame.quit()
