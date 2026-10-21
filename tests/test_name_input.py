import pygame

from typing import Protocol

from src.game.highscore import Highscore
from src.interface.screens.name_input_screen import NameInputScreen
from src.interface.theme.theme_manager import ThemeManager
from src.interface.theme.theme import CLASSIC_THEME


class ScreenProtocol(Protocol):
    """Protocol for screens used by the test."""

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None: ...

    def update(self, delta_time: float) -> None: ...

    def draw(self, screen: pygame.Surface) -> None: ...


class TestGame:
    """Minimal game interface for testing the name input screen."""

    def __init__(self) -> None:
        pygame.init()

        self.running = True
        self.theme_manager = ThemeManager(CLASSIC_THEME)
        self.highscore = Highscore("highscore.json")
        self.highscore.load_score()

        self.test_save_failure = False

        self.screen = pygame.display.set_mode(
            (600, 800),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption("Pac-idol - Test name input")

        self.current_screen: ScreenProtocol = NameInputScreen(
            self,
            12500,
        )

    def change_screen(self, screen: object) -> None:
        """Change the current screen."""
        self.current_screen = screen  # type: ignore[assignment]

    def show_start_screen(self) -> None:
        """Stop the test if the start screen is requested."""
        self.running = False

    def simulate_save_failure(self) -> None:
        """Simulate a failed highscore save."""

        self.highscore.add_score = (
            lambda name, score: False
        )

    def run(self) -> None:
        """Run the test screen."""
        clock = pygame.time.Clock()

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F9
                ):
                    self.simulate_save_failure()

            self.current_screen.events(events)
            self.current_screen.update(clock.get_time() / 1000)
            self.current_screen.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    TestGame().run()
