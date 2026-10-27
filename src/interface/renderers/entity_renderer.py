import pygame

from src.interface.renderers.maze_renderer import MazeRenderer
from src.entities.entity import Entity
from src.entities.pacman import Pacman
from src.interface.renderers.ghost_renderer import GhostRenderer
from src.interface.renderers.pacman_renderer import PacmanRenderer
from src.interface.renderers.animation import EntityAnimator


class EntityRenderer:
    """Coordinate the rendering of game entities."""

    def __init__(self, maze_renderer: MazeRenderer) -> None:
        """Initialize the entity renderers."""
        self.maze_renderer = maze_renderer
        self.animation = EntityAnimator()
        self.ghost_renderer = GhostRenderer(maze_renderer, self.animation)
        self.pacman_renderer = PacmanRenderer(maze_renderer, self.animation)

    def _sync_maze_renderer(self) -> None:
        """Update the maze renderer used by each entity renderer."""
        self.ghost_renderer.maze_renderer = self.maze_renderer
        self.pacman_renderer.maze_renderer = self.maze_renderer

    def _draw_named_ghost(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
        ghost_name: str,
    ) -> None:
        """Draw a ghost using its name."""
        self._sync_maze_renderer()
        self.ghost_renderer.draw(
            screen,
            maze,
            entity,
            ghost_name,
        )

    def draw_ghost(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw Joy using the existing interface."""
        self.draw_joy(screen, maze, entity)

    def draw_joy(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw Joy."""
        self._draw_named_ghost(screen, maze, entity, "joy")

    def draw_gdragon(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw G-DRAGON."""
        self._draw_named_ghost(screen, maze, entity, "gdragon")

    def draw_momo(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw MOMO."""
        self._draw_named_ghost(screen, maze, entity, "momo")

    def draw_louis(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw LOUIS."""
        self._draw_named_ghost(screen, maze, entity, "louis")

    def draw_pacman(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        pacman: Pacman,
    ) -> None:
        """Draw Pac-Man."""
        self._sync_maze_renderer()
        self.pacman_renderer.draw(screen, maze, pacman)
