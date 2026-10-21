from src.interface.theme.theme import Theme


class ThemeManager:
    """Loads and provides the currently active theme."""

    def __init__(self, theme: Theme) -> None:
        self.current_theme = theme

    def get_theme(self) -> Theme:
        return self.current_theme

    def set_theme(self, theme: Theme) -> None:
        self.current_theme = theme
