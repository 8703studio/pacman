import sys
from pathlib import Path

from src import Parser, GameConfig
from src.interface.game_window import GameWindow


def main() -> None:
    if len(sys.argv) != 2:
        print(
            f"Usage: python3 {Path(sys.argv[0]).name} <config.json>",
            file=sys.stderr,
        )
        sys.exit(2)

    config_path = Path(sys.argv[1])
    if not config_path.is_file():
        print(
            f"Erreur : fichier introuvable : {config_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    parser = Parser()
    raw_data = parser.build_config(str(config_path))
    config = GameConfig(**raw_data)

    game = GameWindow(800, 800, config)
    game.run()


if __name__ == "__main__":
    main()
