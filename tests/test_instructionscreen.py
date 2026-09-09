import pygame

from src.interface.screens import InstructionsScreen


class TestGame:
    def __init__(self):
        self.running = True

    def change_screen(self, screen):
        self.current_screen = screen


pygame.init()

screen = pygame.display.set_mode((1024, 1080))
pygame.display.set_caption("Test Instructions Screen")

game = TestGame()
game.current_screen = InstructionsScreen(game)

clock = pygame.time.Clock()

running = True

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    game.current_screen.events(events)
    game.current_screen.update(0)

    screen.fill((0, 0, 0))
    game.current_screen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
