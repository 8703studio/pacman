import random
from mazegenerator import MazeGenerator


class MazeAdapter:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    DIRECTIONS = {
        "up": NORTH,
        "right": EAST,
        "down": SOUTH,
        "left": WEST,
    }

    def __init__(self):
        pass

    def generate_level(
        self,
        level: int,
        seed_base: int,
        width: int,
        height: int,
        max_retries=3
    ) -> list[list[int]]:
        """Generate a maze for the requested level."""
        if level == 1:
            current_seed = seed_base
        else:
            current_seed = random.randint(0, 1000000)

        for attempt in range(max_retries):
            try:
                raw_maze = MazeGenerator(
                    size=(width, height),
                    seed=current_seed,
                    perfect=False,
                    entry_cell=(width // 2, height // 2),
                )
                return raw_maze.maze
            except Exception as e:
                print(f"WARNING, maze generation failed "
                      f"(attempt {attempt+1}): {e}")
                current_seed = random.randint(0, 1000000)

        raise RuntimeError(f"Maze generation failed "
                           f"after {max_retries} attempts")

    def is_wall(
        self,
        maze: list[list[int]],
        x: int,
        y: int,
        direction: str,
    ) -> bool:
        """Return True if a wall blocks the given direction."""
        wall_code = self.DIRECTIONS[direction]
        return bool(maze[y][x] & wall_code)

    def get_neighbor(
        self,
        x: int,
        y: int,
        direction: str,
    ) -> tuple[int, int]:
        """Return the coordinates of the neighboring cell."""

        offsets = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0),
        }

        dx, dy = offsets[direction]
        return x + dx, y + dy

    def get_neighbors(
        self,
        maze: list[list[int]],
        x: int,
        y: int,
    ) -> list[tuple[int, int]]:
        """Return all walkable neighboring cells."""

        neighbors = []

        for direction in self.DIRECTIONS:
            if not self.is_wall(maze, x, y, direction):
                nx, ny = self.get_neighbor(x, y, direction)
                if self.is_walkable(maze, nx, ny):
                    neighbors.append((nx, ny))

        return neighbors

    def get_walkable_cells(
        self,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:

        walkable_cells = []

        for y, line in enumerate(maze):
            for x, _ in enumerate(line):
                neighbors = self.get_neighbors(maze, x, y)

                if neighbors:
                    walkable_cells.append((x, y))

        return walkable_cells

    def get_corners(
        self,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:

        height = len(maze)
        width = len(maze[0])

        corners = [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1)
            ]
        return corners

    def is_walkable(self, maze, x, y):
        if not (0 <= y < len(maze) and 0 <= x < len(maze[0])):
            return False
        if maze[y][x] == 15:
            return False
        return True

    def get_pacgum_positions(self, maze):
        pass

    def get_super_pacgum_positions(self, maze):
        pass

    def get_spawn_positions(self, maze):
        pass
