# from src.engine.physics import Engine
# from src.game.level import Level
from src import GameConfig, Parser
from src import LevelHandler

# maze generator tuples (y, x) (column, line)


def main():
    parser = Parser()
    raw_data = parser.build_config("config.json")
    lvl_handler = LevelHandler()
    lvl_handler.raw_data


if __name__ == "__main__":
    main()
