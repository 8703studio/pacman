from src.interface.game_window import GameWindow
from src.maze.maze_adapter import MazeAdapter


adapter = MazeAdapter()

maze = adapter.generate_level(
    level=1,
    seed_base=42,
    width=21,
    height=21,
)

window = GameWindow(800, 800)
window.maze = maze
window.run()
