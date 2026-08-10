from pydantic import BaseModel, Field
import json
import os


class GameConfig(BaseModel):
    highscore_filename: str = "highscore_filename:"
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


def load_json(filepath: str):
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
        return load_json(cleaned)
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
        except Exception as e:
            print(f"WARNING, invalid data :{e}")
            return {}
