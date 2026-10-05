from mazegenerator import MazeGenerator
from .level import Level


class LevelHandler():
    def __init__(self, config_level: dict[str, int]):
        self.config_data = config_level
        self.level_list = self._create_list_level()
        self.cur_level = 0

    @property
    def current_level(self) -> Level:
        return self.level_list[self.cur_level]

    def _level_maze(self, width: int, height: int,
                    seed_level: int) -> list[list[int]]:

        level_maze = MazeGenerator((width, height), seed=seed_level)
        return level_maze.maze

    def _create_list_level(self) -> list[Level]:
        lev_list = []
        level_config_key, time_key, seed_key = self.config_data

        key_level_list = [_ for _ in self.config_data[level_config_key]]
        timer = self.config_data[time_key]
        seed_level = self.config_data[seed_key]

        for i in key_level_list:
            key1, key2 = i
            width = i[key1]
            height = i[key2]
            mazegen = self._level_maze(width, height, seed_level)

            seed_level += 1
            lev_list.append(Level(mazegen, timer))
        return lev_list

    def next_level(self) -> Level | None:
        if self.cur_level == len(self.level_list) - 1:
            return None
        self.cur_level += 1
        return self.level_list[self.cur_level]
