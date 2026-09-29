# matrice contenant les objets creer a partir du maze


class Game():
    def __init__(self, ghost, engine, level_handler, pacman, config) -> None:
        self.ghost = ghost
        self.engine = engine
        self.levels = level_handler
        self.pacman = pacman
        self.score = 0
        self.pacgum = 0
        self.superpacgum = 0
        self.fruit = 0
        self.config = config
        self.point: dict[str, int] = dict()

    @property
    def score_gum(self):
        pass

    @property
    def score_supergum(self):
        pass

    @property
    def score_fruit(self):
        pass

    @property
    def score_ghost(self):
        pass

    def add_score(self, score: int):
        self.score += score

    def lose_life(self):
        pass

    def update(self):
        pass
