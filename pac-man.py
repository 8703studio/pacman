import mazegenerator as maze
from src.engine.physics import Engine
# from src import Parser,


def main():
    mazegen = maze.MazeGenerator((10, 5))
    mazegen.generate()
    for line in mazegen.maze:
        print(line)
    engine = Engine(mazegen.maze)
    print(engine.is_in_grid((-10, -2)))


if __name__ == "__main__":
    main()
