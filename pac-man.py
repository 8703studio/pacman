# from src.engine.physics import Engine
# from src.game.level import Level

from src import Parser, GameConfig
from src.interface.game_window import GameWindow

# maze generator tuples (y, x) (column, line)


def main() -> None:
    parser = Parser()
    raw_data = parser.build_config("config.json")
    config = GameConfig(**raw_data)

    game = GameWindow(800, 800, config)
    game.run()


if __name__ == "__main__":
    main()
