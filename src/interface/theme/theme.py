import pygame
from dataclasses import dataclass
from src.interface import colors


@dataclass
class Theme:
    name: str

    background_color: pygame.Color
    wall_color: pygame.Color
    text_color: pygame.Color
    player_color: pygame.Color

    ghost_colors: list[pygame.Color]
    ghost_edible_color: pygame.Color

    player_name: str
    ghost_names: list[str]
    pellet_name: str
    super_pellet_name: str

    player_sprite: str | None = None
    ghost_sprites: list[str] | None = None
    wall_texture: str | None = None


CLASSIC_THEME = Theme(
    name="classic",
    background_color=colors.black,
    wall_color=colors.blue,
    text_color=colors.white,
    player_color=colors.yellow,
    ghost_colors=[
        colors.red,
        colors.pink,
        colors.cyan,
        colors.orange,
    ],
    ghost_edible_color=colors.blue,
    player_name="Pac-Man",
    ghost_names=["Blinky", "Pinky", "Inky", "Clyde"],
    pellet_name="Pac-gum",
    super_pellet_name="Super Pac-gum",
)
