import sys
from pathlib import Path
import config
import interface

def main() -> None:
    """Launch the game with the configuration file given as argument."""
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

    try:
        parser = config.Parser()
        raw_data = parser.build_config(str(config_path))
        data = config.GameConfig(**raw_data)

        game = interface.GameWindow(800, 800, data)
        game.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
