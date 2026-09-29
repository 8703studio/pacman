import mazegenerator


class LevelHandler():
    def __init__(self, config_level: dict[str, int]):
        self.raw_data = config_level
        self.level_list = self._create_list_level()

    def _create_list_level(self) -> list[list[list[int]]]:
        levels, seed = self.raw_data.keys()
        width, height = self.raw_data[levels][0]
        print(seed, width, height)
        for i in self.raw_data:
            print(i)
