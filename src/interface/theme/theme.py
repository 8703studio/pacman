from dataclasses import dataclass


@dataclass
class Theme:
    """Represents a visual theme: colors, names, and asset paths."""
    name: str

    background_color: tuple[int, int, int]
    wall_color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    player_color: tuple[int, int, int]
    ghost_colors: list[tuple[int, int, int]]
    ghost_edible_color: tuple[int, int, int]

    player_name: str
    ghost_names: list[str]
    pellet_name: str
    super_pellet_name: str

    player_sprite: str | None = None
    ghost_sprites: list[str] | None = None
    wall_texture: str | None = None
