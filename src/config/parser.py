from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Any
import json
import os


class GameConfig(BaseModel):
    highscore_filename: str = "highscore.json"
    lives: int = Field(default=3, gt=0)
    pacgum: int = Field(default=42, gt=0)
    pointperpacgum: int = Field(default=10, gt=0)
    pointpersuperpacgum: int = Field(default=50, gt=0)
    pointperghost: int = Field(default=200, gt=0)
    levels: list[dict[str, int]] = Field(
        default_factory=lambda:
            [{"width": 21, "height": 21} for _ in range(10)]
    )
    levelsmaxtime: int = Field(default=90, gt=0)
    seed: int = 42

    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, data: Any) -> dict[str, Any]:
        defaults = {
            "highscore_filename": "highscore.json",
            "lives": 3,
            "pacgum": 42,
            "pointperpacgum": 10,
            "pointpersuperpacgum": 50,
            "pointperghost": 200,
            "levels": [
                {"width": 21, "height": 21}
                for _ in range(10)
            ],
            "levelsmaxtime": 90,
            "seed": 42,
        }

        if not isinstance(data, dict):
            print("WARNING: configuration is not a JSON object,"
                  "using defaults")
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
                    print(f"WARNING: invalid '{key}',"
                          f"using default: {default}")
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

                    print(f"WARNING: invalid '{key}',"
                          f"using default: {default}")
                    cleaned[key] = default
                else:
                    cleaned[key] = value

            elif key == "seed":
                if not isinstance(value, int) or isinstance(value, bool):
                    print(f"WARNING: invalid '{key}',"
                          f"using default: {default}")
                    cleaned[key] = default
                else:
                    cleaned[key] = value

            elif key == "levels":
                if not isinstance(value, list):
                    print(f"WARNING: invalid '{key}',"
                          f"using default: {default}")
                    cleaned[key] = default
                else:
                    valid_levels = True
                    for level in value:
                        if (
                            not isinstance(level, dict)
                            or not isinstance(level.get("width"), int)
                            or not isinstance(level.get("height"), int)
                            or level["width"] <= 0
                            or level["height"] <= 0
                        ):
                            valid_levels = False
                            break

                    if not valid_levels:
                        print(f"WARNING: invalid '{key}',"
                              f"using default: {default}")
                        cleaned[key] = default
                    else:
                        cleaned[key] = value

        return cleaned


class Parser:
    """ a remplir
    """
    def build_config(self, filepath: str) -> dict[str,
                                                  int | str | dict[str, int]]:
        """ a remplir
        """
        raw_data = self.load_json(filepath)

        try:
            return GameConfig(**raw_data)
        except ValidationError as e:
            print(f"WARNING, invalid data :{e}")
            return GameConfig()

    def load_json(filepath: str) -> dict:
        """ a remplir
        """
        if not os.path.exists(filepath):
            print(f"WARNING, {filepath} don't exist")
            return {}
        with open(filepath, 'r') as f:
            lines = f.readlines()

        cleaned = "".join([line for line in lines
                          if not line.strip().startswith("#")])

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"WARNING, json syntax error :{e}")
            return {}
        except Exception as e:
            print(f"WARNING, an error occured :{e}")
            return {}
