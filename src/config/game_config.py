from pydantic import BaseModel, Field


class GameConfig(BaseModel):
    highscore_filename: str = "highscore.json"
    lives: int = 3
    pacgum: int = 42
    pointperpacgum: int = 10
    pointpersuperpacgum: int = 50
    pointperghost: int = 200
    levels: list[dict[str, int]] = Field(
        default_factory=lambda: [
            {"width": 21, "height": 21} for _ in range(10)
        ]
    )
    levelsmaxtime: int = 90
    seed: int = 42
