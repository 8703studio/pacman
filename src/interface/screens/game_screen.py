import pygame

from src.interface.menu import GameScreenInterface
from src.interface.hud import HUD
from src.interface.renderers.entity_renderer import EntityRenderer
from src.interface.background import draw_background
from src.entities.ghost_interceptor import GhostInterceptor
from src.entities.entity import EntityDirection
from src.entities.pacman import Pacman
from src.engine.physics import Engine
from src.interface.screens.pause_screen import PauseScreen
from src.engine.input import get_direction
from src.game.game import Game
from src.entities import GhostHandler
from src.interface.renderers.object_renderer import ObjectRenderer
from src.game.gameplay_controller import GameController


class GameScreen:
    """Displays the game screen."""

    def __init__(self, game: GameScreenInterface) -> None:
        """Initialize the game screen."""

        self.game = game

        self.hud = HUD(
            self.game.theme_manager.get_theme()
        )

        self.entity_renderer = EntityRenderer(
            self.game.maze_renderer
        )

        self.ghost = GhostInterceptor((0, 1))
        self.pacman = Pacman()

        level = self.game.level_handler.current_level
        level.start()

        self.pacman.start_pos = (
            len(level.grid) // 2,
            len(level.grid[0]) // 2,
        )
        self.pacman.current_pos = self.pacman.start_pos

        ghost_handler = GhostHandler([self.ghost])
        ghost_handler.set_spawn_ghost(level.corners)

        self.object_renderer = ObjectRenderer(
            self.game.maze_renderer
        )

        engine = Engine(level.grid)

        self.logic = Game(
            ghost_handler,
            engine,
            self.game.level_handler,
            self.pacman,
            self.game.config,
        )
        self.controller = GameController(
            self.logic,
            self.ghost,
            self.game.audio_manager,
        )

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """Handle game events."""

        if self.game.maze is None:
            return

        for event in events:
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                self.game.change_screen(
                    PauseScreen(self.game, self)
                )
                return

            direction = get_direction(event)

            if direction is None:
                continue

            entity_direction = EntityDirection(direction)
            self.logic.pacman.add_move_to_buffer(
                entity_direction
            )

    def update(self, delta_time: float) -> None:
        """Update the game screen."""

        if self.game.maze is None:
            return

        self.controller.update(self.game.maze)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game screen."""

        theme = self.game.theme_manager.get_theme()

        draw_background(
            screen,
            theme.background_color,
            None,
            # theme.background_image,
        )

        if self.game.maze is None:
            return

        self.game.maze_renderer.draw(
            screen,
            self.game.maze,
        )

        self.entity_renderer.maze_renderer = (
            self.game.maze_renderer
        )

        self.hud.render(
            screen,
            self.logic.score,
            self.logic.life,
            self.game.level_handler.cur_level + 1,
            int(self.logic.levels.current_level.remaining_time()),
        )

        self.entity_renderer.draw_ghost(
            screen,
            self.game.maze,
            self.ghost,
        )

        self.entity_renderer.draw_pacman(
            screen,
            self.game.maze,
            self.pacman,
        )

        self.object_renderer.draw(
            screen,
            self.game.maze,
            self.logic.levels.current_level.grid_level,
        )
