import pygame

from src.interface.game_window import GameWindow
from src.interface.screens import GameScreen
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

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.draw()

    pygame.display.flip()

pygame.quit()
