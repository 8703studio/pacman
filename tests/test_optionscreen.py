import pygame

from src.interface.screens import OptionsScreen


class TestGame:
    def __init__(self):
        self.running = True

    def change_screen(self, screen):
        self.current_screen = screen


pygame.init()

screen = pygame.display.set_mode((1024, 950))
pygame.display.set_caption("Test Options Screen")

game = TestGame()
options_screen = OptionsScreen(game)


clock = pygame.time.Clock()

running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    options_screen.events(events)
    options_screen.update(0)

    screen.fill((0, 0, 0))
    options_screen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
