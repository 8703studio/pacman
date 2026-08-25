# import pygame
from mazegenerator import MazeGenerator
# from src import Parser, load_json
# from src.interface.hud import HUD


def main():
    mazegen = MazeGenerator((5, 5))
    mazegen.generate()
    print(mazegen._maze)


if __name__ == "__main__":
    main()
