"""
    the engine class can do the verification like physics, etc.. in game

"""


class Engine():
    def __init__(self, grid) -> None:
        self.grid = grid
        self.opposite_bits = {
            1: 4,
            2: 8,
            4: 1,
            8: 2
        }
        self.bit_direction = {
            (0, -1): 1,
            (1, 0):  2,
            (0, 1):  4,
            (-1, 0): 8
        }

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def is_valid_position(self, direction: tuple[int, int],
                          case: tuple[int, int]) -> bool:
        cy, cx = case
        dir_y, dir_x = direction
        next_case = (cy + dir_y, cx + dir_x)
        ncy, ncx = next_case
        bits = self.bit_direction[direction]

        return (self.is_in_grid(next_case)
                and not self._is_wall(self.grid[cy][cx], bits)
                and not self._is_wall(self.grid[ncy]
                                      [ncx], self._opposite_wall(bits)))

    def _opposite_wall(self, bits_current_case: int) -> int:
        return self.opposite_bits[bits_current_case]

    # this method verify if the entity faced a wall
    def _is_wall(self, case_value: int,
                 bits: int) -> bool:
        print(case_value, bits)
        return (case_value & bits) != 0

    # this method verified if the entity is in the grid
    def is_in_grid(self, case: tuple[int, int]) -> bool:
        y, x = case
        return x >= 0 and x < self.width and y >= 0 and y < self.height
