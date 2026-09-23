from enum import Enum

class GridObject(Enum):
    EMPTY = 0
    GUM = 1
    SUPERGUM = 2
    FRUIT = 3

class Level():
    def __init__(self, level_config, grid_level) -> None:
        self.level_config = level_config
        self.grid_level: list[list[GridObject]]= grid_level

    @property
    def object_grid(self):
        pass

    def consume_object(self):
        pass