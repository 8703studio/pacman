import pygame
from dataclasses import dataclass
from src.interface import colors


@dataclass
class Theme:
    """
    Represents a visual theme used by the game.

    A theme defines the colors, names and assets used to customize
    the game's appearance and interface.
    """

    # Game
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

    # Interface
    menu_text_color: pygame.Color
    menu_selected_color: pygame.Color
    hud_text_color: pygame.Color
    hud_background_color: pygame.Color
    accent_color: pygame.Color
    title_text_color: pygame.Color
    button_color: pygame.Color
    button_color_text: pygame.Color

    # Assets
    player_sprite: str | None = None
    ghost_sprites: list[str] | None = None
    wall_texture: str | None = None
    background_image: str | None = None
    pellet_sprite: str | None = None
    super_pellet_sprite: str | None = None
    victory_background_image: str | None = None
    gameover_background_image: str | None = None


CLASSIC_THEME = Theme(
    name="classic",
    # Game
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
    ghost_names=[
        "Joy",
        "Momo",
        "Louis",
        "G-Dragon",
    ],
    pellet_name="Pac-gum",
    super_pellet_name="Super Pac-gum",
    # Interface
    menu_text_color=colors.classic_text,
    menu_selected_color=colors.classic_selected,
    hud_text_color=colors.classic_text,
    hud_background_color=colors.classic_background,
    accent_color=colors.classic_accent,
    title_text_color=colors.classic_title,
    button_color=colors.classic_button,
    button_color_text=colors.classic_button_text,
    # Assets
    player_sprite="assets/classic/pacman.png",
    ghost_sprites=[
        "assets/classic/ghosts.png",
    ],
    wall_texture="assets/classic/wall.png",
    background_image="src/interface/assets/background/background.png",
    pellet_sprite="assets/classic/pellet.png",
    super_pellet_sprite="assets/classic/super_pellet.png",
    victory_background_image="src/interface/assets/background/background.png",
    gameover_background_image="src/interface/assets/background/background.png",
)


SECOND_THEME = Theme(
    name="pastel",
    # Game
    background_color=colors.white,
    wall_color=colors.orange,
    text_color=colors.black,
    player_color=colors.pink,
    ghost_colors=[
        colors.orange,
        colors.yellow,
        colors.red,
        colors.cyan,
    ],
    ghost_edible_color=colors.blue,
    player_name="Pac-Man",
    ghost_names=[
        "Joy",
        "Momo",
        "Louis",
        "G-Dragon",
    ],
    pellet_name="Pac-gum",
    super_pellet_name="Super Pac-gum",
    # Interface
    menu_text_color=colors.pastel_text,
    menu_selected_color=colors.pastel_selected,
    hud_text_color=colors.pastel_text,
    hud_background_color=colors.pastel_background,
    accent_color=colors.pastel_accent,
    title_text_color=colors.pastel_title,
    button_color=colors.pastel_button,
    button_color_text=colors.pastel_button_text,
    # Assets
    player_sprite="assets/second/pacman.png",
    ghost_sprites=[
        "assets/second/ghosts.png",
    ],
    wall_texture="assets/second/wall.png",
    background_image="src/interface/assets/background/background.png",
    pellet_sprite="assets/second/pellet.png",
    super_pellet_sprite="assets/second/super_pellet.png",
    victory_background_image="src/interface/assets/background/background.png",
    gameover_background_image="src/interface/assets/background/background.png",
)
