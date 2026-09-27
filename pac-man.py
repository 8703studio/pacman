import mazegenerator as maze
from src.engine.physics import Engine
from src.engine.level import Level
from src import GameConfig

# maze generator tuples (y, x) (column, line)


def main():
    mazegen = maze.MazeGenerator((15, 15))
    mazegen.generate()
    for line in mazegen.maze:
        print(line)
    level = Level(mazegen.maze)
    print(level.corners)
    for i in level.grid_level:
        print(i)
    print(level.element_numb)
    level.consume_object((0,0))
    level.consume_object((0,1))
    level.consume_object((0,2))
    level.consume_object((0,3))
    level.consume_object((0,4))
    print(level.element_numb)
    # engine = Engine(mazegen.maze)
    # print(engine.is_in_grid((0, 1)))
    # print(engine.is_wall(4, 4))
    
    


if __name__ == "__main__":
    main()
