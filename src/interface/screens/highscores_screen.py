import pygame

from src.interface.menu import GameInterface
from src.interface.utils import draw_text


class HighscoresScreen:
    """Displays the game's high scores."""

    def __init__(self, game: GameInterface) -> None:
        """Initialize the high scores screen."""
        self.game = game

        theme = self.game.theme_manager.get_theme()

        if theme.background_image is None:
            raise ValueError("Background image is not defined")

        self.background = pygame.image.load(
            theme.background_image
        ).convert()

        self.font = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            36,
        )

        self.title = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            70,
        )

        self.font_button = pygame.font.Font(
            "src/interface/assets/fonts/upheavtt.ttf",
            20,
        )

        self.back_button = pygame.Rect(
            100,
            950,
            100,
            60,
        )

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

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """Handle events from the high scores screen."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.show_start_screen()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.game.show_start_screen()

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

        button_text_rect = button_text.get_rect(
            center=self.back_button.center,
        )

        screen.blit(
            button_text,
            button_text_rect,
        )
