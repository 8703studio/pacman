import random
from mazegenerator import MazeGenerator

class MazeAdapter:
    def __init__(self):
        pass

    def generate_levels(self, level, seed_base, width, height):
        if level == 1:
            current_seed = seed_base
        else:
            current_seed = random.randint(0, 1000000)
        try:
            raw_maze = MazeGenerator(
                size = (width, height),
                seed = current_seed,
                perfect = False
            )
            return raw_maze.maze
        except Exception as e:
                    print(f"WARNING, maze generation failed: {e}")
                    return []
