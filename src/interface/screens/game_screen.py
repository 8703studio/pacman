import pygame

from src.interface.menu import GameScreenInterface
from src.interface.hud import HUD
from src.interface.entity_renderer import EntityRenderer
from src.interface import colors
from src.entities.ghost_interceptor import Ghost_interceptor
from src.entities.entity import Pacman
from tests.test_interceptor import pattern_test


class GameScreen:

    """Displays the game screen."""

    def __init__(self, game: GameScreenInterface) -> None:

        """Initialize the game screen."""

        self.game = game

        self.hud = HUD()

        self.entity_renderer = EntityRenderer(
            self.game.maze_renderer
        )

        self.ghost = Ghost_interceptor((5, 2))
        self.pacman = Pacman((1, 6))

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:

        """Handle events from the game."""

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    pass

    def update(self, delta_time: float) -> None:

        """Update the game screen."""

        self.ghost.grid = pattern_test

        self.ghost.pacman_position = self.pacman.current_pos

        self.ghost.pacman_direction = self.pacman.direction.value

        self.ghost.move()

    def draw(self, screen: pygame.Surface) -> None:

        """Draw the game screen."""

        screen.fill(colors.black)

        if self.game.maze is None:
            return

        self.game.maze_renderer.draw(
            screen,
            self.game.maze,
        )

        self.entity_renderer.draw(
            screen,
            self.game.maze,
            self.ghost,
        )
