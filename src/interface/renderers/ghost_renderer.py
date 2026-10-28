import pygame

from src.interface.renderers.maze_renderer import MazeRenderer
from src.entities.entity import Entity, EntityDirection
from src.enums import EntityState
from src.interface.renderers.animation import EntityAnimator


class GhostRenderer:
    """Render the different ghosts on the maze."""

    GHOST_SPRITES = {
        "joy": "src/interface/assets/ghosts/joy.png",
        "gdragon": "src/interface/assets/ghosts/gdragon-sheets.png",
        "momo": "src/interface/assets/ghosts/momosprite.png",
        "louis": "src/interface/assets/ghosts/louissprite.png",
    }

    def __init__(self, maze_renderer: MazeRenderer,
                 animation: EntityAnimator) -> None:
        """Initialize the ghost renderer."""
        self.maze_renderer = maze_renderer
        self.animation = animation
        self.ghost_frames = {}

        for name, path in self.GHOST_SPRITES.items():
            image = pygame.image.load(path).convert_alpha()
            frame_width = image.get_width() // 6
            frame_height = image.get_height()
            frames = []

            for index in range(6):
                frame = image.subsurface(
                    pygame.Rect(
                        index * frame_width,
                        0,
                        frame_width,
                        frame_height,
                    )
                )
                frames.append(frame)

            self.ghost_frames[name] = frames

    def draw(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
        ghost_name: str = "joy",
    ) -> None:
        """Draw a ghost using its current position and direction."""
        y, x = self.animation.pos(entity)

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

        ghost_size = max(1, int(cell_size * 0.66))

        ghost_image = pygame.transform.scale(
            self.ghost_frames[ghost_name][frame_idx],
            (ghost_size, ghost_size),
        )

        if entity.state == EntityState.WEAK:
            ghost_image.fill(
                (50, 100, 255),
                special_flags=pygame.BLEND_RGB_MULT,
            )

        if entity.state == EntityState.DEAD:
            ghost_image.fill(
                (120, 120, 120),
                special_flags=pygame.BLEND_RGB_MULT,
            )

        screen.blit(
            ghost_image,
            (
                int(pixel_x + (cell_size - ghost_size) / 2),
                int(pixel_y + (cell_size - ghost_size) / 2 - 3),
            ),
        )
