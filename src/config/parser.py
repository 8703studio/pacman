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

    @model_validator(mode="after")
    @classmethod
    def validate_data(cls, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            print("")
            return {}

        default = {
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

        cleaned: dict[str, Any] = {}

        for key, value_default in default.items():
            if key not in data:
                print(f"WARNING, invalid {key}, using {default}")
                cleaned[key] = value_default
                continue

            value = data[key]

            for key, value_default in default.items():
                if key not in data:
                    print(f"WARNING, invalid {key}, using {value_default}")
                    cleaned[key] = value_default
                    continue

                value = data[key]

                if key in ("lives", "pacgum", "pointperpacgum",
                           "pointpersuperpacgum", "pointperghost",
                           "evelsmaxtime"):

                    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                        print(f"WARNING, invalid value for {key}, using {value_default}")
                        cleaned[key] = value_default
                    else:
                        cleaned[key] = value


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


class Parser:
    """ a remplir
    """
    @staticmethod
    def build_config(filepath: str) -> GameConfig:
        """ a remplir
        """
        raw_data = load_json(filepath)

        try:
            return GameConfig(**raw_data)
        except ValidationError as e:
            print(f"WARNING, invalid data :{e}")
            return GameConfig()
