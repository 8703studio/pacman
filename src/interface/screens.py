import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.interface.game_window import GameWindow

from src.interface.menu import MenuStartScreen, MenuOptions, MenuPause
from src.interface.text_renderer import draw_text
from src.interface import colors


class StartScreen:
    """Displays the main menu screen."""
    def __init__(self, game: "GameWindow") -> None:
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        # self.banner = pygame.image.load(
        #     "pac-idol.png"
        # ).convert_alpha()

        self.font = pygame.font.Font('src/interface/assets/fonts/aldotheapache.ttf', 30)
        self.highscore_font = pygame.font.Font('src/interface/assets/fonts/aldotheapache.ttf', 32)
        self.banner_rect = pygame.Rect(100, 150, 824, 450)
        self.subtitle_font = pygame.font.Font(None, 36)
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
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)
        highscore = self.highscore_font.render("HIGH SCORE : 12500", True,
                                               colors.white)
        highscore_rect = highscore.get_rect(centerx=screen.get_width() // 2,
                                            top=20
                                            )

        screen.blit(highscore, highscore_rect)
        pygame.draw.rect(screen, colors.white, self.banner_rect, 3)
        subtitle = self.subtitle_font.render("K-POP ARCADE", True,
                                             colors.white)

        subtitle_rect = subtitle.get_rect(
            centerx=screen.get_width() // 2,
            top=self.banner_rect.bottom + 20
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


class OptionsScreen:
    """Displays the game options screen."""
    def __init__(self, game: "GameWindow") -> None:
        """Initialize the options screen."""
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

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
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)
        self.menu.draw(screen)


class InstructionsScreen:
    """Displays the game instructions."""
    def __init__(self, game: "GameWindow") -> None:
        """Initialize the instructions screen."""
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
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
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        title_surface = self.title.render("INSTRUCTIONS", True, colors.white)

        square_size = 30
        space = 20
        title_y = 50

        total_width = square_size + space + title_surface.get_width() + space + square_size

        start_x = (1024 - total_width) // 2

        left_rect = pygame.Rect(start_x, title_y + (title_surface.get_height() - square_size) // 2,
                                square_size, square_size)

        title_x = start_x + square_size + space

        right_rect = pygame.Rect(
            title_x + title_surface.get_width() + space,
            title_y + (title_surface.get_height() - square_size) // 2,
            square_size,
            square_size
        )

        pygame.draw.rect(screen, colors.white, left_rect, 3)

        draw_text(
            screen,
            "INSTRUCTIONS",
            title_x,
            title_y,
            self.title,
            colors.white
        )

        pygame.draw.rect(screen, colors.white, right_rect, 3)

        draw_text(screen, "Move with the arrow keys", 100, 200, self.font,
                  colors.white)
        draw_text(screen, "Eat the Pac-gums", 100, 240, self.font,
                  colors.white)
        draw_text(screen, "Avoid the ghosts", 100, 280, self.font,
                  colors.white)
        draw_text(screen, "Eat Super Pac-gums", 100, 320, self.font,
                  colors.white)

        pygame.draw.rect(screen, colors.yellow, self.back_button)

        button_text = self.font.render("Retour", True, colors.black)
        button_text_rect = button_text.get_rect(
            center=self.back_button.center
        )

        screen.blit(button_text, button_text_rect)


class PauseScreen:
    """Displays the pause menu."""
    def __init__(self, game: "GameWindow") -> None:
        """Initialize the pause screen."""
        self.game = game

        # self.background = pygame.image.load(
        #     "background-pause.png"
        # ).convert()

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
        screen.fill(colors.black)
        # screen.blit(self.background, (0, 0))

        self.menu.draw(screen)


class HighscoresScreen:
    """Displays the game's high scores."""
    def __init__(self, game: "GameWindow") -> None:
        """Initialize the high scores screen."""
        self.game = game

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        self.back_button = pygame.Rect(100, 800, 100, 60)

        self.rank_x = 150
        self.name_x = 350
        self.score_x = 700

        # self.scores = self.game.highscore.top_score()

        # temp score pour test
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
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        draw_text(screen, "HIGHSCORES", 100, 100, self.title, colors.white)

        draw_text(screen, "RANK", self.rank_x, 200, self.font, colors.white)
        draw_text(screen, "PLAYER", self.name_x, 200, self.font, colors.white)
        draw_text(screen, "SCORE", self.score_x, 200, self.font, colors.white)

        for i, (name, score) in enumerate(self.scores):
            # mettre entry a la place de name, score
            y = 250 + i * 50

            # name = entry["name"]
            # score = entry["score"]

            draw_text(screen, str(i + 1), self.rank_x, y, self.font,
                      colors.white)
            draw_text(screen, name, self.name_x, y, self.font,
                      colors.white)
            draw_text(screen, str(score), self.score_x, y, self.font,
                      colors.white)

        pygame.draw.rect(screen, colors.yellow, self.back_button)

        button_text = self.font.render("Retour", True, colors.black)
        button_text_rect = button_text.get_rect(
            center=self.back_button.center
        )

        screen.blit(button_text, button_text_rect)


class GameOverScreen:
    """Displays the game over screen."""
    def __init__(self, game: "GameWindow") -> None:
        """Initialize the game over screen."""
        self.game = game
        # donnee de test
        self.score = 12500
        self.font = pygame.font.Font(None, 48)
        self.title = pygame.font.Font(None, 80)
        self.font_message = pygame.font.Font(None, 32)

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the game over screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_screen(
                        NameInputScreen(self.game)
                    )

    def update(self, delta_time: float) -> None:
        """Update the game over screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game over screen."""
        screen.fill(colors.black)

        game_over = self.title.render("GAME OVER", True, colors.white)
        game_over_rect = game_over.get_rect(
            center=(screen.get_width() // 2, 300)
        )
        screen.blit(game_over, game_over_rect)

        score = self.font.render(
            f"Final score: {self.score}",
            True,
            colors.white
        )
        score_rect = score.get_rect(
            center=(screen.get_width() // 2, 450)
        )
        screen.blit(score, score_rect)

        message = self.font_message.render(
            "Press ENTER to continue",
            True,
            colors.white
        )
        message_rect = message.get_rect(
            center=(screen.get_width() // 2, 550)
        )
        screen.blit(message, message_rect)


class VictoryScreen:
    """Displays the victory screen."""
    def __init__(self, game: "GameWindow") -> None:
        """Initialize the victory screen."""
        self.game = game
        # donnee de test
        self.score = 12500
        self.font = pygame.font.Font(None, 48)
        self.title = pygame.font.Font(None, 80)
        self.font_message = pygame.font.Font(None, 32)

        # self.background = pygame.image.load(
        #     "background-start.png"
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the victory screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_screen(
                        NameInputScreen(self.game)
                    )

    def update(self, delta_time: float) -> None:
        """Update the victory screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the victory screen."""
        screen.fill(colors.black)

        victory = self.title.render("Victory!", True, colors.white)
        victory_rect = victory.get_rect(
            center=(screen.get_width() // 2, 300)
        )
        screen.blit(victory, victory_rect)

        score = self.font.render(
            f"Final score: {self.score}",
            True,
            colors.white
        )
        score_rect = score.get_rect(
            center=(screen.get_width() // 2, 450)
        )
        screen.blit(score, score_rect)

        message = self.font_message.render(
            "Press ENTER to continue",
            True,
            colors.white
        )
        message_rect = message.get_rect(
            center=(screen.get_width() // 2, 550)
        )
        screen.blit(message, message_rect)


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

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle player name input events."""
        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if self.name.strip():
                        if self.game.highscore.add_score(
                            self.name.strip(),
                            self.game.score
                        ):
                            self.game.highscore.save_score()

                        self.game.change_screen(
                            HighscoresScreen(self.game)
                        )

                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                else:
                    if (
                        len(self.name) < 10
                        and (event.unicode.isalnum() or event.unicode == " ")
                    ):
                        self.name += event.unicode

    def update(self, delta_time: float) -> None:
        """Update the name input screen."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the name input screen."""
        # screen.blit(self.background, (0, 0))
        screen.fill(colors.black)

        font = pygame.font.Font(None, 50)
        title = pygame.font.Font(None, 70)

        text = title.render(
            "ENTER YOUR NAME",
            True,
            colors.white
        )
        text_rect = text.get_rect(
            center=(screen.get_width() // 2, 250)
        )
        screen.blit(text, text_rect)

        name_text = font.render(
            self.name,
            True,
            colors.white
        )
        name_rect = name_text.get_rect(
            center=(screen.get_width() // 2, 400)
        )
        screen.blit(name_text, name_rect)
