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
    menu_text_color=CLASSIC_THEME.menu_text_color,
    menu_selected_color=CLASSIC_THEME.menu_selected_color,
    hud_text_color=CLASSIC_THEME.hud_text_color,
    hud_background_color=CLASSIC_THEME.hud_background_color,
    accent_color=CLASSIC_THEME.accent_color,
    title_text_color=CLASSIC_THEME.title_text_color,
    button_color=CLASSIC_THEME.button_color,
    button_color_text=CLASSIC_THEME.button_color_text,
    player_sprite=None,
    ghost_sprites=None,
    wall_texture=None,
    background_image=None,
    pellet_sprite=None,
    super_pellet_sprite=None,
)


manager.set_theme(test_theme)

print("New theme:", manager.get_theme().name)
print("Player name:", manager.get_theme().player_name)
print("Pellet name:", manager.get_theme().pellet_name)
print("Background:", manager.get_theme().background_image)
