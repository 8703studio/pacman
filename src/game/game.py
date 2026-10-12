# matrice contenant les objets creer a partir du maze
from ..config import GameConfig
from ..engine import Engine
from .level_handler import LevelHandler
from ..entities import GhostHandler, Pacman
# , ghost_handler, engine, level_handler, pacman, config)


class Game():
    def __init__(self, ghost_handler: GhostHandler, engine: Engine,
                 level_handler: LevelHandler,
                 pacman: Pacman, config: GameConfig) -> None:

        self.config: GameConfig = config
        self.ghost = ghost_handler
        self.engine = engine
        self.levels = level_handler
        self.pacman = pacman
        self.score: int = 0
        self.life: int = self.set_life()
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

    def set_life(self) -> int:
        return self.config.lives

    def update(self):
        pass
