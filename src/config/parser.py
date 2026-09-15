import json
import os
from typing import Any


class Parser:
    """Parse and validate the game configuration."""

    def build_config(self, filepath: str) -> dict[str, Any]:
        """Build a validated configuration from a JSON file."""
        raw_data = self.load_json(filepath)
        return self.validate_data(raw_data)

    def validate_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Validate configuration values and apply safe defaults."""
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
            print(
                "WARNING: configuration is not a JSON object, "
                "using defaults"
            )
            return defaults

        cleaned: dict[str, Any] = {}

        for key, default in defaults.items():
            if key not in data:
                print(
                    f"WARNING: missing '{key}', " f"using default: {default}"
                )
                cleaned[key] = default
                continue

            value = data[key]

            if key == "highscore_filename":
                if not isinstance(value, str):
                    print(
                        f"WARNING: invalid '{key}', "
                        f"using default: {default}"
                    )
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
                if (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value <= 0
                ):
                    print(
                        f"WARNING: invalid '{key}', "
                        f"using default: {default}"
                    )
                    cleaned[key] = default
                else:
                    cleaned[key] = value

            elif key == "seed":
                if not isinstance(value, int) or isinstance(value, bool):
                    print(
                        f"WARNING: invalid '{key}', "
                        f"using default: {default}"
                    )
                    cleaned[key] = default
                else:
                    cleaned[key] = value

            elif key == "levels":
                if not isinstance(value, list):
                    print(
                        f"WARNING: invalid '{key}', "
                        f"using default: {default}"
                    )
                    cleaned[key] = default
                else:
                    valid_levels = True

                    for level in value:
                        if (
                            not isinstance(level, dict)
                            or not isinstance(level.get("width"), int)
                            or isinstance(level.get("width"), bool)
                            or not isinstance(level.get("height"), int)
                            or isinstance(level.get("height"), bool)
                            or level["width"] <= 0
                            or level["height"] <= 0
                        ):
                            valid_levels = False
                            break

                    if not valid_levels:
                        print(
                            f"WARNING: invalid '{key}', "
                            f"using default: {default}"
                        )
                        cleaned[key] = default
                    else:
                        cleaned[key] = value

        return cleaned

    def load_json(self, filepath: str) -> dict[str, Any]:
        """Load a JSON file and ignore lines starting with #."""
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
                print("WARNING: configuration is not a JSON object")
                return {}

            return data

        except json.JSONDecodeError as error:
            print(f"WARNING: JSON syntax error: {error}")
            return {}
        except OSError as error:
            print(f"WARNING: unable to read configuration: {error}")
            return {}
