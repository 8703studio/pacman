import pygame
import mazegenerator as maze

from src.interface.screens.start_screen import StartScreen
from src.interface.theme.theme import CLASSIC_THEME
from src.interface.theme.theme_manager import ThemeManager
from src.interface.maze_renderer import MazeRenderer
from tests.test_interceptor import pattern_test


class TestGame:

    def __init__(self):

        self.running = True

        self.theme_manager = ThemeManager(CLASSIC_THEME)

        mazegen = maze.MazeGenerator(
            (21, 21),
            seed=42,
            perfect=False,
            entry_cell=(10, 10),
        )

        self.maze = mazegen.maze

        print("MAZE SIZE :", len(self.maze), "x", len(self.maze[0]))

        self.maze_renderer = MazeRenderer(
            width=1024,
            height=1080,
            hud_height=130,
            theme=self.theme_manager.get_theme(),
            margin=5,
        )

        self.pattern_test = pattern_test

    def change_screen(self, screen):

        self.current_screen = screen

    def show_start_screen(self):

        self.current_screen = StartScreen(self)


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
