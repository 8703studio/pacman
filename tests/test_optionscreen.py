import pygame

from src.interface.screens import OptionsScreen


pygame.init()

screen = pygame.display.set_mode((1024, 1080))
pygame.display.set_caption("Test Options")

options_screen = OptionsScreen()

running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    options_screen.events(events)
    options_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
