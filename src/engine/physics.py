from enum import Enum

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

    @property
    def width(self) -> int:
        return len(self.grid[0])

    @property
    def height(self) -> int:
        return len(self.grid)

    def is_valid_position(self, next_case: tuple[int, int],
                          case: tuple[int, int], bits: int) -> bool:
        
        pass

    def opposite_wall(self, bits_current_case: int) -> int:
        return self.opposite_bits[bits_current_case]
            

    # this method verify if the entity faced a wall
    def is_wall(self, case_value: int,
                bits: int) -> bool:
        print(case_value, bits)
        return (case_value & bits) != 0

    # this method verified if the entity is in the grid
    def is_in_grid(self, case: tuple[int, int]) -> bool:
        y, x = case
        return x >= 0 and x < self.width and y >= 0 and y < self.height
