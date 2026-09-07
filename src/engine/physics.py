"""
    the engine class can do the verification like physics, etc.. in game

    the class have  2 property x_len and y_len

    x_len = len of 1 line of the matrix

    y_len = len of the matrix
"""


class Engine():
    def __init__(self, grid) -> None:
        self.grid = grid

    @property
    def x_len(self) -> int:
        return len(self.grid[0])

    @property
    def y_len(self) -> int:
        return len(self.grid)

    def is_valid_position(self, next_case: tuple[int, int],
                          case: tuple[int, int]) -> bool:
        pass

    # this method verify if the entity faced a wall
    # direction contain dx, dy, bits
    def is_wall(self, case: tuple[int, int],
                direction: tuple[int, int, int]) -> bool:
        x, y = case
        x_dir, y_dir, bits = direction

        return self.is_in_grid(case) and self.grid[y][x] & bits

    # this method verified if the entity is in the grid
    def is_in_grid(self, case: tuple[int, int]) -> bool:
        x, y = case
        if x > 0 and x < self.x_len and y > 0 and y < self.y_len:
            return True
        return False
