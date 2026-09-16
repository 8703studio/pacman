import pygame

from src.interface.game_window import GameWindow
from src.maze.maze_adapter import MazeAdapter

adapter = MazeAdapter()

maze = adapter.generate_level(
    level=1,
    seed_base=42,
    width=21,
    height=21,
)

window = GameWindow(1024, 1200)

window.maze = maze

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.screen.fill(window.theme_manager.get_theme().background_color)

    window.maze_renderer.draw(
        window.screen,
        window.maze,
    )

    pygame.display.flip()

pygame.quit()
