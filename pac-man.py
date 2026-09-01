from mazegenerator import MazeGenerator
# from src import Parser, load_json
# from src.interface.hud import HUD


def main():
    mazegen = MazeGenerator((5, 5))
    mazegen.generate()
    for line in mazegen.maze:
        print(line)


if __name__ == "__main__":
    main()
