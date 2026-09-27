from enum import Enum




    # matrice contenant les objets creer a partir du maze

class Game():
    def __init__(self, ghost, engine, level, pacman) -> None:
        self.ghost = ghost
        self.engine = engine
        self.level = level
        self.pacman = pacman

    def pacman_update(self):
        pass

    def update_grid(self):
        pass

    def ghost_update(self):
        pass
    
    def update(self):
        pass