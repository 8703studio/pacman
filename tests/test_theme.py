from src.interface.theme.theme import CLASSIC_THEME, Theme
from src.interface.theme.theme_manager import ThemeManager


manager = ThemeManager(CLASSIC_THEME)

print("Theme:", manager.get_theme().name)

test_theme = Theme(
    name="test",
    background_color=CLASSIC_THEME.background_color,
    wall_color=CLASSIC_THEME.wall_color,
    text_color=CLASSIC_THEME.text_color,
    player_color=CLASSIC_THEME.player_color,
    ghost_colors=CLASSIC_THEME.ghost_colors,
    ghost_edible_color=CLASSIC_THEME.ghost_edible_color,
    player_name="Test",
    ghost_names=CLASSIC_THEME.ghost_names,
    pellet_name="Test pellet",
    super_pellet_name="Test super pellet",
)

manager.set_theme(test_theme)

print("New theme:", manager.get_theme().name)
