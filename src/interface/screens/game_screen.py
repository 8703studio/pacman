import pygame

from src.interface.menu import GameScreenInterface
from src.interface.hud import HUD
from src.interface.renderers.entity_renderer import EntityRenderer
from src.interface.background import draw_background
from src.entities import (
    GhostHandler,
    GhostChaser,
    GhostGlutton,
    GhostInterceptor,
    GhostTactic,
    Pacman,
)
from src.entities.entity import EntityDirection
from src.engine.physics import Engine
from src.interface.screens.pause_screen import PauseScreen
from src.engine.input import get_direction
from src.game.game import Game
from src.interface.renderers.object_renderer import ObjectRenderer
from src.game.gameplay_controller import GameController
from src.game.level_handler import LevelHandler
from src.enums import StateGame
from src.interface.screens.end_game_screen import EndGameScreen


class GameScreen:
    """Displays the game screen."""

    def __init__(self, game: GameScreenInterface) -> None:
        """Initialize the game screen."""

        self.game = game

        self.game.level_handler = LevelHandler(self.game.config.level_data())
        self.game.maze = self.game.level_handler.current_level.grid

        self.hud = HUD(self.game.theme_manager.get_theme())

        self.entity_renderer = EntityRenderer(self.game.maze_renderer)

        level = self.game.level_handler.current_level
        level.start()

        engine = Engine(level.grid)

        self.ghost = GhostInterceptor(level.corners[0])
        self.ghost.engine = engine

        self.ghosts = [
            self.ghost,
            GhostChaser(engine),
            GhostGlutton(engine),
            GhostTactic(engine),
        ]

        self.pacman = Pacman()

        self.pacman.start_pos = (
            len(level.grid) // 2,
            len(level.grid[0]) // 2,
        )
        self.pacman.current_pos = self.pacman.start_pos

        ghost_handler = GhostHandler(self.ghosts)
        ghost_handler.set_spawn_ghost(level.corners)

        self.object_renderer = ObjectRenderer(self.game.maze_renderer)

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.logic.pause_game()
                self.game.change_screen(PauseScreen(self.game, self))
                return

            direction = get_direction(event)

            if direction is None:
                continue

            entity_direction = EntityDirection(direction)
            self.logic.pacman.add_move_to_buffer(entity_direction)

    def update(self, delta_time: float) -> None:
        """Update the game screen."""

        if self.game.maze is None:
            return

        if self.logic.gamestate == StateGame.PAUSE:
            self.logic.resume_game()

        self.game.maze = self.logic.levels.current_level.grid
        self.controller.update(self.game.maze)
        self.game.maze = self.logic.levels.current_level.grid

        if not self.logic.run:
            self.game.change_screen(
                EndGameScreen(
                    self.game,
                    self.logic.gamestate == StateGame.VICTORY,
                    self.logic.score,
                )
            )

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

        self.object_renderer.draw(
            screen,
            self.game.maze,
            self.logic.levels.current_level.grid_level,
        )

        self.entity_renderer.maze_renderer = self.game.maze_renderer

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
            self.ghosts[0],
        )

        self.entity_renderer.draw_gdragon(
            screen,
            self.game.maze,
            self.ghosts[1],
        )

        self.entity_renderer.draw_momo(
            screen,
            self.game.maze,
            self.ghosts[2],
        )

        self.entity_renderer.draw_pacman(
            screen,
            self.game.maze,
            self.pacman,
        )
