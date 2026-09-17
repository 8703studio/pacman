import json
import os
from typing import Any


class Parser:
    """
    parse and validate the game config file
    """

    def build_config(self, filepath: str) -> dict[str, Any]:
        raw_data = self.load_json(filepath)
        return self.validate_data(raw_data)

    def validate_data(self, data: dict[str, Any]) -> dict[str, Any]:
        defaults: dict[str, Any] = {
            "highscore_filename": "highscore.json",
            "lives": 3,
            "pacgum": 42,
            "pointperpacgum": 10,
            "pointpersuperpacgum": 50,
            "pointperghost": 200,
            "levels": [{"width": 21, "height": 21} for _ in range(10)],
            "levelsmaxtime": 90,
            "seed": 42,
        }

        if not isinstance(data, dict):
            print("WARNING: config is not a JSON object, using defaults")
            return defaults

        cleaned: dict[str, Any] = {}

        for key, default in defaults.items():
            if key not in data:
                print(f"WARNING: missing '{key}', using default: {default}")
                cleaned[key] = default
                continue

            value = data[key]

            if key == "highscore_filename":
                if not isinstance(value, str):
                    print(f"WARNING: '{key}' invalid, fallback {default}")
                    cleaned[key] = default
                else:
                    cleaned[key] = value

            elif key in {
                "lives",
                "pacgum",
                "pointperpacgum",
                "pointpersuperpacgum",
                "pointperghost",
                "levelsmaxtime",
            }:
                ok = (
                    isinstance(value, int)
                    and not isinstance(value, bool)
                    and value > 0
                )
                if not ok:
                    print(f"WARNING: '{key}' invalid, fallback {default}")
                cleaned[key] = value if ok else default

            elif key == "seed":
                if isinstance(value, int) and not isinstance(value, bool):
                    cleaned[key] = value
                else:
                    print(f"WARNING: '{key}' invalid, fallback {default}")
                    cleaned[key] = default

            elif key == "levels":
                if not isinstance(value, list) or not value:
                    print(
                        f"WARNING: '{key}' invalid or empty, "
                        f"fallback {default}"
                    )
                    cleaned[key] = default
                elif not all(self._is_valid_level(level) for level in value):
                    print(
                        f"WARNING: '{key}' invalid or empty, "
                        f"fallback {default}"
                    )
                    cleaned[key] = default
                else:
                    cleaned[key] = value

        return cleaned

    def _is_valid_level(self, level: Any) -> bool:
        if not isinstance(level, dict):
            return False

        level_width = level.get("width")
        level_height = level.get("height")

        return (
            isinstance(level_width, int)
            and not isinstance(level_width, bool)
            and level_width > 0
            and isinstance(level_height, int)
            and not isinstance(level_height, bool)
            and level_height > 0
        )

    def load_json(self, filepath: str) -> dict[str, Any]:
        if not os.path.exists(filepath):
            print(f"WARNING: {filepath} does not exist")
            return {}

        try:
            with open(filepath, "r") as file:
                lines = file.readlines()

            cleaned = "".join(
                line for line in lines if not line.strip().startswith("#")
            )
            data = json.loads(cleaned)

            if not isinstance(data, dict):
                print("WARNING: config is not a JSON object")
                return {}
            return data

        except json.JSONDecodeError as error:
            print(f"WARNING: JSON syntax error: {error}")
            return {}
        except UnicodeDecodeError as error:
            print(f"WARNING: bad encoding: {error}")
            return {}
        except OSError as error:
            print(f"WARNING: can't read config: {error}")
            return {}
