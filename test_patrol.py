from src import (GhostTactic, Engine, Level,
                 Pacman, GridObject, EntityDirection)
import mazegenerator as mazegen

if __name__ == "__main__":

    mazegene = mazegen.MazeGenerator((15, 15))
    level = Level(mazegene.maze, 90)
    engine = Engine(level.grid)
    pacman = Pacman()
    tactic = GhostTactic(engine)
    tactic.start_pos = (14, 14)
    tactic.define_zone()
    print(tactic.coord_zone)


