import pygame

from src.interface.menu import GameScreenInterface
from src.interface.hud import HUD
from src.interface.entity_renderer import EntityRenderer
from src.interface import colors
from src.entities.ghost_interceptor import Ghost_interceptor
from src.entities.entity import Pacman
from src.maze.maze_adapter import MazeAdapter
from src.engine.input import get_direction


class GameScreen:
    """Displays the game screen."""

    def __init__(self, game: GameScreenInterface) -> None:
        """Initialize the game screen."""
        self.game = game
        self.hud = HUD()
        self.maze_adapter = MazeAdapter()
        self.entity_renderer = EntityRenderer(self.game.maze_renderer)
        self.ghost = Ghost_interceptor((0, 1))
        print("CREATION :", self.ghost.current_pos)
        self.pacman = Pacman((1, 6))

    def events(self, events):
        if self.game.maze is None:
            return

        direction_names = {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right",
        }

        for event in events:
            direction = get_direction(event)

            if direction is None:
                continue

            print("TUPLE DIRECTION :", direction)

            direction_name = direction_names[direction]

            print("TOUCHE :", event.key)
            print("DIRECTION :", direction_name)
            print("POSITION AVANT :", self.pacman.current_pos)

            if not self.maze_adapter.is_wall(
                self.game.maze,
                self.pacman.current_pos,
                direction_name,
            ):
                self.pacman.move(direction)
                print("POSITION APRES :", self.pacman.current_pos)
            else:
                print("MUR : déplacement impossible")

            print("--------------------")

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

        cell_size = self.game.maze_renderer.get_cell_size(self.game.maze)

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
