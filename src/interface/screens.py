import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.interface.game_window import GameWindow

from src.interface.menu import MenuStartScreen, MenuOptions, MenuPause
from src.interface.hud import HUD
from src.interface.text_renderer import draw_text
from src.interface import colors


class StartScreen:
    """Displays the main menu screen."""

    def __init__(self, game: "GameWindow") -> None:
        self.game = game

        self.background = pygame.image.load(
            "src/interface/assets/background/background.png"
        ).convert()

        self.background = pygame.transform.scale(self.background, (1024, 1080))

        # self.banner = pygame.image.load(
        #     "pac-idol.png"
        # ).convert_alpha()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 30
        )
        self.highscore_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 32
        )
        self.banner_rect = pygame.Rect(100, 150, 824, 450)
        self.subtitle_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 36
        )
        self.menu = MenuStartScreen()

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the main menu."""
        action = self.menu.handle_events(events)

        if action == "Start Game":
            self.game.change_screen(GameScreen(self.game))

        elif action == "View Highscores":
            self.game.change_screen(HighscoresScreen(self.game))

        elif action == "Instructions":
            self.game.change_screen(InstructionsScreen(self.game))

        elif action == "Options":
            self.game.change_screen(OptionsScreen(self.game))

        elif action == "Exit":
            self.game.running = False

    def update(self, delta_time: float) -> None:
        """Update the main menu screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the main menu screen."""
        screen.blit(self.background, (0, 0))
        # screen.fill(colors.black)

        highscore = self.highscore_font.render(
            "HIGH SCORE : 12500", True, colors.white
        )

        highscore_rect = highscore.get_rect(
            centerx=screen.get_width() // 2, top=30
        )

        screen.blit(highscore, highscore_rect)

        pygame.draw.rect(screen, colors.white, self.banner_rect, 3)

        subtitle = self.subtitle_font.render(
            "K-POP ARCADE", True, colors.white
        )

        subtitle_rect = subtitle.get_rect(
            centerx=screen.get_width() // 2, top=self.banner_rect.bottom + 20
        )

        screen.blit(subtitle, subtitle_rect)

        # banner_rect = self.banner.get_rect()
        # banner_rect.centerx = screen.get_rect().centerx
        # banner_rect.top = 100

        # screen.blit(self.banner, banner_rect)

        self.menu.draw(screen)


class GameScreen:
    """Displays the game screen."""

    def __init__(self, game: "GameWindow") -> None:
        """Initialize the game screen."""
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the game"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.change_screen(PauseScreen(self.game))

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if self.back_button.collidepoint(event.pos):
            #         self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the game screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game screen."""
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)
        self.hud = HUD()


class OptionsScreen:
    """Displays the game options screen."""

    def __init__(self, game: "GameWindow") -> None:
        """Initialize the options screen."""
        self.game = game

        self.background = pygame.image.load(
            "src/interface/assets/background/background.png"
        ).convert()

        self.background = pygame.transform.scale(self.background, (1024, 1080))

        self.menu = MenuOptions()

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the options menu."""
        action = self.menu.handle_events(events)

        if action == "Back":
            self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the options screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the options screen."""
        screen.blit(self.background, (0, 0))
        # screen.fill(colors.black)
        self.menu.draw(screen)


class InstructionsScreen:
    """Displays the game instructions."""

    def __init__(self, game: "GameWindow") -> None:
        """Initialize the instructions screen."""
        self.game = game

        self.background = pygame.image.load(
            "src/interface/assets/background/background.png"
        ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        # self.move_icon = pygame.image.load(
        #     "assets/icons/move.png"
        # ).convert_alpha()

        # self.pacgum_icon = pygame.image.load(
        #     "assets/icons/pacgum.png"
        # ).convert_alpha()

        # self.ghost_icon = pygame.image.load(
        #     "assets/icons/ghost.png"
        # ).convert_alpha()

        # self.super_pacgum_icon = pygame.image.load(
        #     "assets/icons/super_pacgum.png"
        # ).convert_alpha()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 36
        )
        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 70
        )
        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 20
        )
        self.back_button = pygame.Rect(100, 800, 100, 60)
        self.icon_left_rect = pygame.Rect(380, 30, 30, 30)
        self.icon_right_rect = pygame.Rect(750, 30, 30, 30)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the instructions screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen(StartScreen(self.game))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the instructions screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the instructions screen."""
        screen.blit(self.background, (0, 0))
        # screen.fill(colors.black)

        title_text = "INSTRUCTIONS"
        title_width = self.title.size(title_text)[0]

        icon_size = 30
        space = 20

        total_width = icon_size + space + title_width + space + icon_size

        title_x = (screen.get_width() - total_width) // 2
        title_y = 100

        left_icon_x = title_x
        right_icon_x = title_x + icon_size + space + title_width + space

        title_x += icon_size + space

        title_surface = self.title.render(
            title_text,
            True,
            colors.white,
        )

        icon_y = title_y + (title_surface.get_height() - icon_size) // 2

        pygame.draw.rect(
            screen,
            colors.white,
            pygame.Rect(
                left_icon_x,
                icon_y,
                icon_size,
                icon_size,
            ),
            3,
        )

        draw_text(
            screen,
            title_text,
            title_x,
            title_y,
            self.title,
            colors.white,
        )

        pygame.draw.rect(
            screen,
            colors.white,
            pygame.Rect(
                right_icon_x,
                icon_y,
                icon_size,
                icon_size,
            ),
            3,
        )

        icon_positions = [
            (50, 200),
            (50, 240),
            (50, 280),
            (50, 320),
        ]

        for x, y in icon_positions:
            pygame.draw.rect(
                screen,
                colors.white,
                pygame.Rect(x, y, icon_size, icon_size),
                3,
            )

        # Real icons - uncomment when the assets are ready
        #
        # icons = [
        #     self.move_icon,
        #     self.pacgum_icon,
        #     self.ghost_icon,
        #     self.super_pacgum_icon,
        # ]
        #
        # for icon, (x, y) in zip(icons, icon_positions):
        #
        #     screen.blit(icon, (x, y))

        draw_text(
            screen,
            "Move Pac-idol with the arrow keys",
            100,
            200,
            self.font,
            colors.white,
        )

        draw_text(
            screen, "Eat the Pac-gums", 100, 240, self.font, colors.white
        )

        draw_text(
            screen,
            "Avoid the rival ghosts idols",
            100,
            280,
            self.font,
            colors.white,
        )

        draw_text(
            screen, "Eat Super Pac-gums", 100, 320, self.font, colors.white
        )

        pygame.draw.rect(screen, colors.yellow, self.back_button)

        button_text = self.font_button.render("Back", True, colors.black)

        button_text_rect = button_text.get_rect(center=self.back_button.center)

        screen.blit(button_text, button_text_rect)


class PauseScreen:
    """Displays the pause menu."""

    def __init__(self, game: "GameWindow") -> None:
        """Initialize the pause screen."""
        self.game = game

        self.background = pygame.image.load(
            "src/interface/assets/background/background.png"
        ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        self.menu = MenuPause()

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the pause menu."""
        action = self.menu.handle_events(events)

        if action == "Resume":
            pass

        elif action == "Return to main menu":
            self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the pause screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pause screen."""
        # screen.fill(colors.black)

        screen.blit(self.background, (0, 0))

        self.menu.draw(screen)


class HighscoresScreen:
    """Displays the game's high scores."""

    def __init__(self, game: "GameWindow") -> None:
        """Initialize the high scores screen."""
        self.game = game

        self.background = pygame.image.load(
            "src/interface/assets/background/background.png"
        ).convert()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 30
        )

        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 70
        )

        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 20
        )

        self.back_button = pygame.Rect(100, 800, 100, 60)

        self.rank_x = 150
        self.name_x = 350
        self.score_x = 700

        # High scores
        # self.scores = self.game.highscore.top_score()

        # Temporary scores for testing
        self.scores = [
            ("EMILIE", 12500),
            ("PLAYER2", 10000),
            ("PLAYER3", 8500),
            ("PLAYER4", 7000),
            ("PLAYER5", 6000),
            ("PLAYER6", 5000),
            ("PLAYER7", 4000),
            ("PLAYER8", 3000),
            ("PLAYER9", 2000),
            ("PLAYER10", 1000),
        ]

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the high scores screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen(StartScreen(self.game))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.game.change_screen(StartScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the high scores screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the high scores screen."""
        screen.blit(self.background, (0, 0))

        title_width = self.title.size("HALL OF FAME")[0]
        title_x = (screen.get_width() - title_width) // 2

        draw_text(
            screen,
            "HALL OF FAME",
            title_x,
            100,
            self.title,
            colors.white,
        )

        draw_text(
            screen,
            "RANK",
            self.rank_x,
            200,
            self.font,
            colors.yellow,
        )

        draw_text(
            screen,
            "IDOL",
            self.name_x,
            200,
            self.font,
            colors.yellow,
        )

        draw_text(
            screen,
            "SCORE",
            self.score_x,
            200,
            self.font,
            colors.yellow,
        )

        for i, (name, score) in enumerate(self.scores):
            y = 250 + i * 52

            draw_text(
                screen,
                str(i + 1),
                self.rank_x,
                y,
                self.font,
                colors.white,
            )

            draw_text(
                screen,
                name,
                self.name_x,
                y,
                self.font,
                colors.white,
            )

            draw_text(
                screen,
                str(score),
                self.score_x,
                y,
                self.font,
                colors.white,
            )

        pygame.draw.rect(
            screen,
            colors.yellow,
            self.back_button,
        )

        button_text = self.font_button.render(
            "Back",
            True,
            colors.black,
        )

        button_text_rect = button_text.get_rect(center=self.back_button.center)

        screen.blit(
            button_text,
            button_text_rect,
        )


class EndGameScreen:
    """Displays the end game screen."""

    def __init__(
        self,
        game: "GameWindow",
        victory: bool,
    ) -> None:
        """Initialize the end game screen."""
        self.game = game
        self.victory = victory

        # Donnée de test
        self.score = 12500

        self.font = pygame.font.Font(None, 48)
        self.title = pygame.font.Font(None, 70)
        self.font_message = pygame.font.Font(None, 32)

        self.continue_button = pygame.Rect(412, 650, 200, 60)

        # self.background = pygame.image.load(
        #     "background-end.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the end game screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_screen(NameInputScreen(self.game))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.continue_button.collidepoint(event.pos):
                        self.game.change_screen(NameInputScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the end game screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the end game screen."""
        screen.fill(colors.black)

        if self.victory:
            title_text = "VICTORY!"
        else:
            title_text = "GAME OVER"

        title = self.title.render(
            title_text,
            True,
            colors.white,
        )

        title_rect = title.get_rect(center=(screen.get_width() // 2, 300))

        screen.blit(title, title_rect)

        score = self.font.render(
            f"Final score: {self.score}",
            True,
            colors.white,
        )

        score_rect = score.get_rect(center=(screen.get_width() // 2, 450))

        screen.blit(score, score_rect)

        pygame.draw.rect(
            screen,
            colors.yellow,
            self.continue_button,
        )

        button_text = self.font_message.render(
            "CONTINUE",
            True,
            colors.black,
        )

        button_text_rect = button_text.get_rect(
            center=self.continue_button.center
        )

        screen.blit(button_text, button_text_rect)


class NameInputScreen:
    """Handles player name input for the high score."""

    def __init__(self, game: "GameWindow") -> None:
        """Initialize the name input screen."""
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.name = ""
        self.score = 12500

        self.font = pygame.font.Font(None, 50)
        self.title = pygame.font.Font(None, 70)
        self.message_font = pygame.font.Font(None, 32)

        self.input_rect = pygame.Rect(312, 350, 400, 70)
        self.continue_button = pygame.Rect(412, 500, 200, 60)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle player name input events."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._submit_name()

                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                else:
                    if len(self.name) < 10 and (
                        event.unicode.isalnum() or event.unicode == " "
                    ):
                        self.name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.continue_button.collidepoint(event.pos):
                        self._submit_name()

    def _submit_name(self) -> None:
        """Submit the player name."""
        name = self.name.strip()

        if not name:
            return

        # if self.game.highscore.add_score(
        #     name,
        #     self.game.score,
        # ):
        #     self.game.highscore.save_score()

        self.game.change_screen(HighscoresScreen(self.game))

    def update(self, delta_time: float) -> None:
        """Update the name input screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the name input screen."""
        screen.fill(colors.black)

        title = self.title.render(
            "ENTER YOUR NAME",
            True,
            colors.white,
        )

        title_rect = title.get_rect(center=(screen.get_width() // 2, 200))

        screen.blit(title, title_rect)

        pygame.draw.rect(
            screen,
            colors.white,
            self.input_rect,
            2,
        )

        name_text = self.font.render(
            self.name,
            True,
            colors.white,
        )

        name_rect = name_text.get_rect(center=self.input_rect.center)

        screen.blit(name_text, name_rect)

        message = self.message_font.render(
            "10 characters maximum",
            True,
            colors.white,
        )

        message_rect = message.get_rect(center=(screen.get_width() // 2, 450))

        screen.blit(message, message_rect)

        pygame.draw.rect(
            screen,
            colors.yellow,
            self.continue_button,
        )

        button_text = self.message_font.render(
            "CONTINUE",
            True,
            colors.black,
        )

        button_text_rect = button_text.get_rect(
            center=self.continue_button.center
        )

        screen.blit(button_text, button_text_rect)
