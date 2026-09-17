import pygame

from src.interface.menu import (
    GameInterface,
    MenuStartScreen,
    MenuOptions,
    MenuPause,
)
from src.interface.hud import HUD
from src.interface.utils import draw_text
from src.entities.ghost_interceptor import Ghost_interceptor
from src.entities.entity import Pacman
from src.interface.entity_renderer import EntityRenderer

# from src.interface.utils import get_center
from src.interface import colors


class StartScreen:
    """Displays the start screen."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the start screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

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
        self.menu = MenuStartScreen(self.game)

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
        theme = self.game.theme_manager.get_theme()
        # screen.fill(colors.black)

        highscore = self.highscore_font.render(
            "HIGH SCORE : 12500", True, theme.menu_text_color
        )

        highscore_rect = highscore.get_rect(
            centerx=screen.get_width() // 2, top=30
        )

        screen.blit(highscore, highscore_rect)

        pygame.draw.rect(screen, theme.menu_text_color, self.banner_rect, 3)

        subtitle = self.subtitle_font.render(
            "K-POP ARCADE", True, theme.title_text_color
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

    def __init__(self, game: GameInterface) -> None:
        """Initialize the game screen."""
        self.game = game
        self.hud = HUD()
        self.entity_renderer = EntityRenderer(self.game.maze_renderer)
        self.ghost = Ghost_interceptor((2, 5))
        self.pacman = Pacman((1, 6))
        # theme = self.game.theme_manager.get_theme()

        # if theme.background_image is None:
        #     raise ValueError("Background image is not defined")

        # self.background = pygame.image.load(
        #     theme.background_image
        # ).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the game"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
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
        # theme = self.game.theme_manager.get_theme()

        self.game.maze_renderer.draw(
            screen,
            self.game.maze,
        )
        self.entity_renderer.draw(
            screen,
            self.game.maze,
            self.ghost,
        )


class OptionsScreen:
    """Displays the game options screen."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the options screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

        self.background = pygame.transform.scale(self.background, (1024, 1080))

        self.menu = MenuOptions(self.game)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the options menu."""
        action = self.menu.handle_events(events)

        for event in events:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_BACKSPACE
            ):
                action = "Back"

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

    def __init__(self, game: GameInterface) -> None:
        """Initialize the instructions screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 26
        )

        self.small_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 24
        )

        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 60
        )

        self.section_font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 30
        )

        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 20
        )

        self.back_button = pygame.Rect(100, 950, 100, 55)

    def events(self, events: list[pygame.event.Event]) -> None:
        """Handle events from the instructions screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
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

        theme = self.game.theme_manager.get_theme()

        # Title
        title_text = "HOW TO PLAY"

        title = self.title.render(
            title_text,
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(
            centerx=screen.get_width() // 2,
            top=100,
        )

        screen.blit(title, title_rect)

        # Main instruction panel
        panel_rect = pygame.Rect(
            100,
            180,
            824,
            430,
        )

        pygame.draw.rect(
            screen,
            theme.menu_text_color,
            panel_rect,
            3,
        )

        # Instruction cards
        cards = [
            (
                pygame.Rect(140, 220, 340, 160),
                "MOVE",
                "ARROW KEYS",
            ),
            (
                pygame.Rect(544, 220, 340, 160),
                "PAC-GUM",
                "EAT",
            ),
            (
                pygame.Rect(140, 410, 340, 160),
                "POWER",
                "+50 PTS",
            ),
            (
                pygame.Rect(544, 410, 340, 160),
                "RIVAL IDOLS",
                "AVOID",
            ),
        ]

        for rect, title_text, description in cards:
            pygame.draw.rect(
                screen,
                theme.title_text_color,
                rect,
                2,
            )

            card_title = self.section_font.render(
                title_text,
                True,
                theme.title_text_color,
            )

            card_title_rect = card_title.get_rect(
                centerx=rect.centerx,
                top=rect.top + 15,
            )

            screen.blit(card_title, card_title_rect)

            # Placeholder for future image
            placeholder = pygame.Rect(
                rect.centerx - 25,
                rect.top + 55,
                50,
                50,
            )

            pygame.draw.rect(
                screen,
                theme.menu_text_color,
                placeholder,
                2,
            )

            card_description = self.small_font.render(
                description,
                True,
                theme.menu_text_color,
            )

            description_rect = card_description.get_rect(
                centerx=rect.centerx,
                bottom=rect.bottom - 15,
            )

            screen.blit(
                card_description,
                description_rect,
            )

        # Score system
        draw_text(
            screen,
            "SCORE SYSTEM",
            100,
            650,
            self.section_font,
            theme.title_text_color,
        )

        draw_text(
            screen,
            "PAC-GUM",
            100,
            700,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "10 PTS",
            650,
            700,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "POWER PELLET",
            100,
            735,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "50 PTS",
            650,
            735,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "GHOSTS",
            100,
            770,
            self.small_font,
            theme.menu_text_color,
        )

        draw_text(
            screen,
            "200 PTS",
            650,
            770,
            self.small_font,
            theme.menu_text_color,
        )

        # Lightsticks
        draw_text(
            screen,
            "LIGHTSTICKS",
            100,
            825,
            self.section_font,
            theme.title_text_color,
        )

        lightstick_positions = [
            200,
            300,
            400,
            500,
            600,
            700,
            800,
        ]

        for x in lightstick_positions:
            pygame.draw.rect(
                screen,
                theme.menu_text_color,
                pygame.Rect(
                    x - 20,
                    870,
                    40,
                    55,
                ),
                2,
            )

        # Back button
        pygame.draw.rect(
            screen,
            theme.button_color,
            self.back_button,
        )

        button_text = self.font_button.render(
            "BACK",
            True,
            theme.button_color_text,
        )

        button_text_rect = button_text.get_rect(center=self.back_button.center)

        screen.blit(
            button_text,
            button_text_rect,
        )


class PauseScreen:
    """Displays the pause menu."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the pause screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

        # self.background = pygame.transform.scale(
        #     self.background, (1024, 1080)
        # )

        self.font = pygame.font.Font(None, 32)
        self.title = pygame.font.Font(None, 60)
        self.menu = MenuPause(self.game)

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

    def __init__(self, game: GameInterface) -> None:
        """Initialize the high scores screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 36
        )

        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 70
        )

        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf", 20
        )

        self.back_button = pygame.Rect(100, 950, 100, 60)

        self.rank_center = 280
        self.name_center = 512
        self.score_center = 744

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
                if event.key == pygame.K_BACKSPACE:
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
        theme = self.game.theme_manager.get_theme()

        # Title
        title_text = "HALL OF FAME"

        title = self.title.render(
            title_text,
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(
            centerx=screen.get_width() // 2,
            top=100,
        )

        screen.blit(title, title_rect)

        # Column titles
        rank_width = self.font.size("RANK")[0]

        draw_text(
            screen,
            "RANK",
            self.rank_center - rank_width // 2,
            220,
            self.font,
            theme.title_text_color,
        )

        name_width = self.font.size("IDOL")[0]

        draw_text(
            screen,
            "IDOL",
            self.name_center - name_width // 2,
            220,
            self.font,
            theme.title_text_color,
        )

        score_width = self.font.size("SCORE")[0]

        draw_text(
            screen,
            "SCORE",
            self.score_center - score_width // 2,
            220,
            self.font,
            theme.title_text_color,
        )

        # Scores
        for i, (name, score) in enumerate(self.scores):
            y = 320 + i * 50

            rank_width = self.font.size(str(i + 1))[0]

            draw_text(
                screen,
                str(i + 1),
                self.rank_center - rank_width // 2,
                y,
                self.font,
                theme.menu_text_color,
            )

            name_width = self.font.size(name)[0]

            draw_text(
                screen,
                name,
                self.name_center - name_width // 2,
                y,
                self.font,
                theme.menu_text_color,
            )

            score_width = self.font.size(str(score))[0]

            draw_text(
                screen,
                str(score),
                self.score_center - score_width // 2,
                y,
                self.font,
                theme.menu_text_color,
            )

        # Back button
        pygame.draw.rect(
            screen,
            theme.button_color,
            self.back_button,
        )

        button_text = self.font_button.render(
            "Back",
            True,
            theme.button_color_text,
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
        game: GameInterface,
        victory: bool,
    ) -> None:
        """Initialize the end game screen."""
        self.game = game
        self.victory = victory

        theme = self.game.theme_manager.get_theme()

        if self.victory:
            background_path = theme.victory_background_image
        else:
            background_path = theme.gameover_background_image

        if background_path is None:
            raise ValueError("End game background is not defined")

        self.background = pygame.image.load(background_path).convert()

        self.background = pygame.transform.scale(self.background, (1024, 1080))

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
        screen.blit(self.background, (0, 0))
        theme = self.game.theme_manager.get_theme()

        if self.victory:
            title_text = "VICTORY!"
        else:
            title_text = "GAME OVER"

        title = self.title.render(
            title_text,
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(center=(screen.get_width() // 2, 300))

        screen.blit(title, title_rect)

        score = self.font.render(
            f"Final score: {self.score}",
            True,
            theme.menu_text_color,
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
            theme.menu_text_color,
        )

        button_text_rect = button_text.get_rect(
            center=self.continue_button.center
        )

        screen.blit(button_text, button_text_rect)


class NameInputScreen:
    """Handles player name input for the high score."""

    def __init__(
        self,
        game: GameInterface,
    ) -> None:
        """Initialize the name input screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(theme.background_image).convert()

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
        screen.blit(self.background, (0, 0))
        theme = self.game.theme_manager.get_theme()

        title = self.title.render(
            "ENTER YOUR NAME",
            True,
            theme.menu_text_color,
        )

        title_rect = title.get_rect(center=(screen.get_width() // 2, 200))

        screen.blit(title, title_rect)

        pygame.draw.rect(
            screen,
            theme.menu_text_color,
            self.input_rect,
            2,
        )

        name_text = self.font.render(
            self.name,
            True,
            theme.menu_text_color,
        )

        name_rect = name_text.get_rect(center=self.input_rect.center)

        screen.blit(name_text, name_rect)

        message = self.message_font.render(
            "10 characters maximum",
            True,
            theme.menu_text_color,
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
            theme.menu_text_color,
        )

        button_text_rect = button_text.get_rect(
            center=self.continue_button.center
        )

        screen.blit(button_text, button_text_rect)
