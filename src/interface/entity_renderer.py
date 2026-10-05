import pygame

from src.interface.maze_renderer import MazeRenderer
from src.entities.entity import EntityDirection, Entity, Pacman


class EntityRenderer:
    """Render the game entities on the maze generated."""

    def __init__(self, maze_renderer: MazeRenderer) -> None:
        """Initialize the entity renderer for the maze."""
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

        self.pacman_image = pygame.image.load(
            "src/interface/assets/pacman/pacman-sprite-2.png"
        ).convert_alpha()

        pacman_frame_width = self.pacman_image.get_width() // 3
        pacman_frame_height = self.pacman_image.get_height()
        self.pacman_frames = []

        for index in range(3):
            frame = self.pacman_image.subsurface(
                pygame.Rect(
                    index * pacman_frame_width,
                    0,
                    pacman_frame_width,
                    pacman_frame_height,
                )
            )
            self.pacman_frames.append(frame)

    def draw_ghost(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        entity: Entity,
    ) -> None:
        """Draw an entity on its current maze position."""
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

        ghost_size = int(cell_size * 0.58)

        ghost_image = pygame.transform.scale(
            self.ghost_frames[frame_idx],
            (ghost_size, ghost_size),
        )

        screen.blit(
            ghost_image,
            (
                int(pixel_x + (cell_size - ghost_size) / 2),
                int(pixel_y + (cell_size - ghost_size) / 2 - 3),
            ),
        )

    def draw_pacman(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        pacman: Pacman,
    ) -> None:
        """Draw Pac-Man on its current maze position."""
        y, x = pacman.current_pos

        pixel_x, pixel_y = self.maze_renderer.get_cell_position(
            maze,
            x,
            y,
        )

        cell_size = self.maze_renderer.get_cell_size(maze)
        pacman_size = int(cell_size * 0.58)

        print("DIRECTION PACMAN :", pacman.direction)
        frame_idx = 1

        if pacman.direction == EntityDirection.LEFT:
            pacman_image = pygame.transform.flip(
                self.pacman_frames[frame_idx],
                True,
                False,
            )
        elif pacman.direction == EntityDirection.UP:
            pacman_image = pygame.transform.rotate(
                self.pacman_frames[frame_idx],
                90,
            )
        elif pacman.direction == EntityDirection.DOWN:
            pacman_image = pygame.transform.rotate(
                self.pacman_frames[frame_idx],
                -90,
            )
        else:
            pacman_image = self.pacman_frames[frame_idx]

        pacman_image = pygame.transform.scale(
            pacman_image,
            (pacman_size, pacman_size),
        )

        screen.blit(
            pacman_image,
            (
                int(pixel_x + (cell_size - pacman_size) / 2),
                int(pixel_y + (cell_size - pacman_size) / 2),
            ),
        )
