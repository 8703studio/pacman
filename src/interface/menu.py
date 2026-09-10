import pygame
from src.interface import colors


class MenuStartScreen:
    """Displays the main menu."""
    def __init__(self) -> None:
        """Initialize the menu."""
        self.font = pygame.font.Font('src/interface/assets/fonts/aldotheapache.ttf', 48)
        self.small_font = pygame.font.Font('src/interface/assets/fonts/aldotheapache.ttf', 32)

        self.options = [
            "Start Game",
            "View Highscores",
            "Instructions",
            "Options",
            "Exit"
            ]
        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

    def handle_events(
        self, events: list[pygame.event.Event]
    ) -> str | None:
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
            self.small_font.size(option)[0]
            for option in self.options
        ) + spacing * (len(self.options) - 1)

        x = (screen.get_width() - total_width) // 2

        for i, option in enumerate(self.options):

            color = colors.yellow if i == self.selected else colors.white

            option_text = self.small_font.render(option, True, color)

            option_rect = option_text.get_rect(left=x, top=750)

            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)

            x = option_rect.right + spacing


class MenuOptions:
    """Displays the options menu."""
    def __init__(self) -> None:
        """Initialize the menu."""
        self.font = pygame.font.Font(None, 48)
        self.options = [
            "Sound",
            "Music",
            "Theme",
            "Back",
        ]
        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

    def handle_events(
        self, events: list[pygame.event.Event]
    ) -> str | None:
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

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.font.render(option, True, color)

            option_rect = option_text.get_rect(midtop=(start_x + i * 180, 800))
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)


class MenuPause:
    """Displays the pause menu."""
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 48)
        self.options = [
            "Resume game",
            "Return to main menu",
        ]
        self.selected = 0
        self.option_rects: list[pygame.Rect] = []

    def handle_events(
        self, events: list[pygame.event.Event]
    ) -> str | None:
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

        for i, option in enumerate(self.options):
            color = colors.yellow if i == self.selected else colors.white

            option_text = self.font.render(option, True, color)

            option_rect = option_text.get_rect(midtop=(start_x + i * 180, 800))
            self.option_rects.append(option_rect)
            screen.blit(option_text, option_rect)
