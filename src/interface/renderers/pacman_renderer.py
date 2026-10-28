import pygame

from src.interface.renderers.maze_renderer import MazeRenderer
from src.entities.entity import EntityDirection
from src.entities.pacman import Pacman
from src.interface.renderers.animation import EntityAnimator


class PacmanRenderer:
    """Render Pac-Man on the generated maze."""
    def __init__(self, maze_renderer: MazeRenderer,
                 animation: EntityAnimator) -> None:
        """Initialize the Pac-Man renderer."""
        self.maze_renderer = maze_renderer
        self.animation = animation

        self.pacman_image = pygame.image.load(
            "src/interface/assets/pacman/pacman-sprite-2.png"
        ).convert_alpha()

        frame_width = self.pacman_image.get_width() // 3
        frame_height = self.pacman_image.get_height()
        self.pacman_frames = []

        for index in range(3):
            frame = self.pacman_image.subsurface(
                pygame.Rect(
                    index * frame_width,
                    0,
                    frame_width,
                    frame_height,
                )
            )
            self.pacman_frames.append(frame)

    def draw(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        pacman: Pacman,
    ) -> None:
        """Draw Pac-Man at its current maze position."""
        y, x = self.animation.pos(pacman)

        origin_x, origin_y = self.maze_renderer.get_cell_position(maze, 0, 0)
        cell_size = self.maze_renderer.get_cell_size(maze)
        pixel_x = origin_x + x * cell_size
        pixel_y = origin_y + y * cell_size

        pacman_size = int(cell_size * 0.6)
        t = self.animation.progress(pacman)

        if t >= 1.0:
            frame_idx = 1
        elif t < 0.5:
            frame_idx = 2 - int(t * 4)
        else:
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
