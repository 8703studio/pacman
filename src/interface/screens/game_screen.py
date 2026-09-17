import pygame

from src.interface.menu import GameScreenInterface
from src.interface.hud import HUD
from src.interface.entity_renderer import EntityRenderer
from src.interface import colors
from src.entities.ghost_interceptor import Ghost_interceptor
from src.entities.entity import Pacman
from src.maze.maze_adapter import MazeAdapter


class GameScreen:
    """Displays the game screen."""

    def __init__(self, game: GameScreenInterface) -> None:
        """Initialize the game screen."""
        self.game = game
        self.hud = HUD()
        self.maze_adapter = MazeAdapter()
        self.entity_renderer = EntityRenderer(
            self.game.maze_renderer
        )
        self.ghost = Ghost_interceptor((5, 2))
        print("CREATION :", self.ghost.current_pos)
        self.pacman = Pacman((1, 6))

    def events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """Handle events from the game."""
        if self.game.maze is None:
            return

        directions = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right",
        }

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key not in directions:
                    continue

                direction_name = directions[event.key]

                y, x = self.pacman.current_pos

                if not self.maze_adapter.is_wall(
                    self.game.maze,
                    x,
                    y,
                    direction_name,
                ):
                    self.pacman.move(
                        {
                            "up": (-1, 0),
                            "down": (1, 0),
                            "left": (0, -1),
                            "right": (0, 1),
                        }[direction_name]
                    )

    def update(self, delta_time: float) -> None:
        """Update the game screen."""
        if self.game.maze is None:
            return

        self.ghost.grid = self.game.maze
        self.ghost.pacman_position = self.pacman.current_pos
        self.ghost.pacman_direction = self.pacman.direction
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

        cell_size = self.game.maze_renderer.get_cell_size(
            self.game.maze
        )

        pixel_x, pixel_y = self.game.maze_renderer.get_cell_position(
            self.game.maze,
            self.pacman.current_pos[1],
            self.pacman.current_pos[0],
        )

        pygame.draw.circle(
            screen,
            colors.yellow,
            (
                int(pixel_x + cell_size / 2),
                int(pixel_y + cell_size / 2),
            ),
            int(cell_size / 3),
        )
