import pygame

from typing import Optional, Protocol

from src.interface.theme.theme_manager import ThemeManager
from src.interface.theme.theme import CLASSIC_THEME, SECOND_THEME
from src.interface.maze_renderer import MazeRenderer


class GameInterface(Protocol):
    """Interface required by the interface screens."""

    theme_manager: ThemeManager
    running: bool

    def change_screen(self, screen: object) -> None:
        """Change the current interface screen."""

    def show_start_screen(self) -> None:
        """Return to the start screen."""


class GameScreenInterface(GameInterface, Protocol):
    """Interface required by the game screen."""

    maze_renderer: MazeRenderer
    maze: Optional[list[list[int]]]


class MenuStartScreen:
    """Displays the main menu."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the menu."""
        self.game = game
        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 48
        )
        self.small_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 24
        )

        self.options = [
            "Start Game",
            "View Highscores",
            "Instructions",
            "Options",
            "Exit",
        ]
        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        """Handle events of main menu."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            return self.options[i]

        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu."""
        self.option_rects = []

        x = 80
        spacing = 35

        total_width = sum(
            self.small_font.size(option)[0] for option in self.options
        ) + spacing * (len(self.options) - 1)

        x = (screen.get_width() - total_width) // 2

        theme = self.game.theme_manager.get_theme()

        for i, option in enumerate(self.options):

            color = (
                theme.menu_selected_color
                if i == self.selected
                else theme.menu_text_color
            )

            option_text = self.small_font.render(option, True, color)

            option_rect = option_text.get_rect(left=x, top=750)

            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)

            x = option_rect.right + spacing


class MenuOptions:
    """Displays the options menu."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the menu."""
        self.game = game
        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 44
        )

        self.options = [
            "Sound",
            "Music",
            "Theme",
            "Back",
        ]

        self.values = {
            "Sound": True,
            "Music": True,
            "Theme": (
                "Pastel K-POP"
                if self.game.theme_manager.get_theme() == SECOND_THEME
                else "Classic K-POP"
            ),
        }

        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        """Handle keyboard and mouse events."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)

                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)

                elif event.key == pygame.K_LEFT:
                    self._change_value(-1)

                elif event.key == pygame.K_RIGHT:
                    self._change_value(1)

                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "Back":
                        return "Back"

            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            self.selected = i

                            if self.options[i] == "Back":
                                return "Back"

                            self._change_value(1)

        return None

    def _change_value(self, direction: int) -> None:
        """Change the value of the selected option."""
        option = self.options[self.selected]

        if option == "Sound":
            self.values["Sound"] = not self.values["Sound"]

        elif option == "Music":
            self.values["Music"] = not self.values["Music"]

        elif option == "Theme":
            if self.values["Theme"] == "Classic K-POP":
                self.values["Theme"] = "Pastel K-POP"
                self.game.theme_manager.set_theme(SECOND_THEME)
            else:
                self.values["Theme"] = "Classic K-POP"
                self.game.theme_manager.set_theme(CLASSIC_THEME)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the options menu."""
        start_y = 300

        self.option_rects = []

        for i, option in enumerate(self.options):
            theme = self.game.theme_manager.get_theme()
            color = (
                theme.menu_selected_color
                if i == self.selected
                else theme.menu_text_color
            )

            if option == "Sound":
                value = "ON" if self.values["Sound"] else "OFF"
                text = f"Sound : {value}"

            elif option == "Music":
                text = "Music : COMING SOON"

            elif option == "Theme":
                text = f"Theme : {self.values['Theme']}"

            else:
                text = option

            option_text = self.font.render(text, True, color)

            option_rect = option_text.get_rect(
                center=(screen.get_width() // 2, start_y + i * 80)
            )

            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)


class MenuPause:
    """Displays the pause menu."""

    def __init__(self, game: GameInterface) -> None:
        self.game = game
        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 48
        )
        self.options = [
            "Resume",
            "Return to main menu",
        ]
        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

    def handle_events(self, events: list[pygame.event.Event]) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(event.pos):
                        self.selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            return self.options[i]

        return None

    def draw(self, screen: pygame.Surface) -> None:
        start_x = 260
        self.option_rects = []

        theme = self.game.theme_manager.get_theme()

        for i, option in enumerate(self.options):
            color = (
                theme.menu_selected_color
                if i == self.selected
                else theme.menu_text_color
            )

            option_text = self.font.render(option, True, color)

            option_rect = option_text.get_rect(midtop=(start_x + i * 180, 800))
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)
