import pygame

from src.interface.maze_renderer import MazeRenderer
from src.entities.entity import EntityDirection, Entity


class EntityRenderer:
    """Render the game entities on the maze generated"""

    def __init__(self, maze_renderer: MazeRenderer) -> None:
        """Initialize the entity renderer for the maze"""
        self.maze_renderer = maze_renderer

        self.ghost_image = pygame.image.load(
            "src/interface/assets/ghosts/joy.png"
        ).convert_alpha()

        frame_width = self.ghost_image.get_width() // 6
        frame_height = self.ghost_image.get_height()

        self.ghost_frames = []

        for index in range(6):
            frame = self.ghost_image.subsurface(
                pygame.Rect(
                    index * frame_width,
                    0,
                    frame_width,
                    frame_height,
                )
            )
            self.ghost_frames.append(frame)

    def draw(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw an entity on it's current maze position."""
        y, x = entity.current_pos

        pixel_x, pixel_y = self.maze_renderer.get_cell_position(
            maze,
            x,
            y,
        )

        cell_size = self.maze_renderer.get_cell_size(maze)

        frame_idx = 0

        if entity.direction == EntityDirection.UP:
            frame_idx = 1
        elif entity.direction == EntityDirection.DOWN:
            frame_idx = 2
        elif entity.direction == EntityDirection.RIGHT:
            frame_idx = 3
        elif entity.direction == EntityDirection.LEFT:
            frame_idx = 4

        ghost_size = int(cell_size * 0.7)

        ghost_image = pygame.transform.scale(
            self.ghost_frames[frame_idx],
            (ghost_size, ghost_size),
        )

        screen.blit(
            ghost_image,
            (
                int(pixel_x + (cell_size - ghost_size) / 2),
                int(pixel_y + (cell_size - ghost_size) / 2),
            ),
        )
