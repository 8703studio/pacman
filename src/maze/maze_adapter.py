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

    OFFSETS = {
        "up": (-1, 0),
        "right": (0, 1),
        "down": (1, 0),
        "left": (0, -1),
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
        pos: tuple[int, int],
        direction: str,
    ) -> bool:
        """Return True if a wall blocks the given direction."""
        y, x = pos
        wall_code = self.DIRECTIONS[direction]
        return bool(maze[y][x] & wall_code)

    def get_neighbor(
        self,
        pos: tuple[int, int],
        direction: str,
    ) -> tuple[int, int]:
        """Return the coordinates of the neighboring cell."""

        y, x = pos
        dy, dx = self.OFFSETS[direction]
        return (y + dy, x + dx)

    def get_neighbors(
        self,
        maze: list[list[int]],
        pos: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return all walkable neighboring cells."""

        neighbors = []

        for direction in self.DIRECTIONS:
            if not self.is_wall(maze, pos, direction):
                npos = self.get_neighbor(pos, direction)
                if self.is_walkable(maze, npos):
                    neighbors.append(npos)

        return neighbors

    def get_walkable_cells(
        self,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:

        walkable_cells = []

        for y, line in enumerate(maze):
            for x, _ in enumerate(line):
                neighbors = self.get_neighbors(maze, (y, x))

                if neighbors:
                    walkable_cells.append((y, x))

        return walkable_cells

    def get_corners(
        self,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:

        height = len(maze)
        width = len(maze[0])

        corners = [
            (0, 0),
            (0, width - 1),
            (height - 1, 0),
            (height - 1, width - 1)
            ]
        return corners

    def is_walkable(self, maze, pos):
        y, x = pos
        if not (0 <= y < len(maze) and 0 <= x < len(maze[0])):
            return False
        if maze[y][x] == 15:
            return False
        return True

    def get_pacgum_positions(self, maze):
        spawns = self.get_spawn_positions(maze)
        exclued_positions = set(spawns["ghosts"])
        exclued_positions.add(spawns["pacman"])
        cases = self.get_walkable_cells(maze)
        return [cell for cell in cases if cell not in exclued_positions]

    def get_super_pacgum_positions(self, maze):
        return self.get_corners(maze)

    def get_spawn_positions(self, maze):
        height = len(maze)
        width = len(maze[0])
        pacman_pos = (height // 2, width // 2)
        ghost_positions = self.get_corners(maze)
        return {
            "pacman": pacman_pos,
            "ghosts": ghost_positions
        }
