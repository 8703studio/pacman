from mazegenerator import MazeGenerator
# from src import Parser, load_json


def main():
    mazegen = MazeGenerator((5, 5))
    mazegen.generate()
    print(mazegen._maze)


if __name__ == "__main__":
    main()
