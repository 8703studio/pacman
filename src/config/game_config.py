from pydantic import BaseModel, Field


class GameConfig(BaseModel):
    highscore_filename: str = "highscore.json"
    lives: int = 3
    pacgum: int = 42
    point_per_pacgum: int = 10
    point_per_superpacgum: int = 50
    point_per_ghost: int = 200
    levels: list[dict[str, int]] = Field(
        default_factory=lambda: [
            {"width": 21, "height": 21} for _ in range(10)
        ]
    )
    levels_max_time: int = 90
    seed: int = 42
