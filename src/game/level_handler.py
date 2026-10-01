from mazegenerator import MazeGenerator
from level import Level

class LevelHandler():
    def __init__(self, config_level: dict[str, int]):
        self.config_data = config_level
        self.level_list = []
        self.cur_level = 0

    def _level_maze(self, width: int, height: int,
                    seed_level: int) -> list[list[int]]:

        level_maze = MazeGenerator((width, height), seed=seed_level)
        return level_maze.maze

    def _create_list_level(self) -> None:
        level_config_key, time_key, seed_key = self.config_data
        key1, key2 = level_config_key

        timer = self.config_data[time_key]
        seed_level = self.config_data[seed_key]
        width = self.config_data[key1]
        height = self.config_data[key2]

        for i in self.config_data:
            mazegen = self._level_maze(width, height, seed_level)
            seed_level += 1
            self.level_list.append(Level(mazegen, timer))

    @property
    def current_level(self) -> Level:
        return self.level_list[self.cur_level]

    def next_level(self) -> Level | None:
        if self.cur_level == len(self.level_list) - 1:
            return None
        self.cur_level += 1
        return self.level_list[self.cur_level]
