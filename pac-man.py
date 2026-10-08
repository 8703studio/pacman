# from src.engine.physics import Engine
# from src.game.level import Level, Game
from src import (Parser, LevelHandler, GhostHandler, GhostChaser, 
                 GhostInterceptor, GhostRandom,
                 GhostTactic, GameConfig, Game)
# maze generator tuples (y, x) (column, line)


def main():
    parser = Parser()
    raw_data = parser.build_config("config.json")
    level_handler = LevelHandler(raw_data.level_data())
    ghost_list = [
        GhostChaser(),
        GhostInterceptor(),
        GhostRandom(),
        GhostTactic()
    ]

    print(level_handler.current_level.corners)
    ghost_handler = GhostHandler(ghost_list)
    ghost_handler.set_spawn_ghost(level_handler.current_level.corners)

    for level in level_handler.level_list:
        print(level)


if __name__ == "__main__":
    main()
