# matrice contenant les objets creer a partir du maze
from ..config import GameConfig
from .level_handler import LevelHandler
# , ghost_handler, engine, level_handler, pacman, config)


class Game():
    def __init__(self, ghost_handler, engine,
                 level_handler, pacman, config) -> None:
        self.ghost = ghost_handler
        self.engine = engine
        self.levels: LevelHandler = level_handler
        self.pacman = pacman
        self.score: int = 0
        self.life: int = 0
        self.config: GameConfig = config
        self.point: dict[str, int] = dict()
        self.run: bool = True

    @property
    def object_point(self):
        config_game = self.config.game_data()
        print(config_game)

    def main_game(self):
        while self.run:
            pass

    def add_score(self, score: int):
        self.score += score

    def lose_life(self):
        self.life -= 1

    def update(self):
        pass
