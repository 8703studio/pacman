import mazegenerator as maze
from src.engine.physics import Engine

# from src import GameConfig

# maze generator tuples (y, x) (column, line)


def main():
    mazegen = maze.MazeGenerator((10, 5))
    mazegen.generate()
    for line in mazegen.maze:
        print(line)
    engine = Engine(mazegen.maze)
    print(engine.is_in_grid((9, 2)))
    print(engine.is_wall((4, 9), (1, 0, mazegen.maze[3][9])))


if __name__ == "__main__":
    main()
