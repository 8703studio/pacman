import pygame

from src.interface.game_window import GameWindow
from src.interface.screens.game_screen import GameScreen
from src.maze.maze_adapter import MazeAdapter


adapter = MazeAdapter()

maze = adapter.generate_level(
    level=1,
    seed_base=42,
    width=21,
    height=21,
)

window = GameWindow(600, 800)

window.maze = maze
window.current_screen = GameScreen(window)

while window.running:

    window.handle_events()

    window.update(0)

    window.screen = pygame.display.get_surface()

    window.draw()

    pygame.display.flip()

pygame.quit()
