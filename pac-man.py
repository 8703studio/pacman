# from src.engine.physics import Engine
# from src.game.level import Level
from src import Parser
from src import LevelHandler

# maze generator tuples (y, x) (column, line)


def main():
    parser = Parser()
    raw_data = parser.build_config("config.json")
    print()
    lvl_handler = LevelHandler(raw_data.level_data())
    for i in lvl_handler.level_list:
        print(i.grid_level)


if __name__ == "__main__":
    main()
