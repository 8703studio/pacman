import pygame

from src.maze.maze_adapter import MazeAdapter
from src.interface.theme.theme import Theme
from src.interface import colors


class MazeRenderer:
    """Renders the maze and its game entities."""

    def __init__(
        self,
        width: int,
        height: int,
        theme: Theme,
        hud_height: int = 130,
        margin: int = 5,
    ) -> None:
        """Initialize the maze renderer dimensions."""
        self.width = width
        self.height = height
        self.hud_height = hud_height
        self.margin = margin
        self.theme = theme

    def get_cell_size(self, maze: list[list[int]]) -> float:
        """Calculate the cell size to fit the maze in the game window."""
        rows = len(maze)
        cols = len(maze[0])
        available_width = self.width - 2 * self.margin
        available_height = self.height - self.hud_height - 2 * self.margin
        cell_size = min(
            available_width / cols,
            available_height / rows,
        )
        return cell_size

    def get_cell_position(
        self,
        maze: list[list[int]],
        x: int,
        y: int,
    ) -> tuple[float, float]:
        """Return the pixel position of a maze cell."""
        rows = len(maze)
        cols = len(maze[0])

        cell_size = self.get_cell_size(maze)

        total_width = cell_size * cols
        total_height = cell_size * rows

        offset_x = (self.width - total_width) / 2 + self.margin

        offset_y = (
            self.hud_height
            + (self.height - self.hud_height - total_height) / 2
            + self.margin
        )

        pixel_x = offset_x + x * cell_size
        pixel_y = offset_y + y * cell_size

        return pixel_x, pixel_y

    @staticmethod
    def _draw_segment(
        screen: pygame.Surface,
        color: pygame.Color,
        start: tuple[float, float],
        end: tuple[float, float],
        width: float,
        border_radius: int,
    ) -> None:
        """Draw an axis-aligned wall segment as a thick rect
        with rounded caps."""
        x1, y1 = start
        x2, y2 = end
        half = width / 2

        if y1 == y2:  # segment horizontal
            left = min(x1, x2) - half
            rect = pygame.Rect(left, y1 - half, abs(x2 - x1) + width, width)
        else:  # segment vertical
            top = min(y1, y2) - half
            rect = pygame.Rect(x1 - half, top, width, abs(y2 - y1) + width)

        pygame.draw.rect(screen, color, rect, border_radius=border_radius)

    def draw(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
    ) -> None:
        """Draw the maze walls on the screen."""
        rows = len(maze)
        cols = len(maze[0])
        cell_size = self.get_cell_size(maze)
        total_width = cell_size * cols
        total_height = cell_size * rows
        offset_x = (self.width - total_width) / 2 + self.margin
        offset_y = (
            self.hud_height
            + (self.height - self.hud_height - total_height) / 2
            + self.margin
        )

        wall_width = 14
        highlight_width = 4

        layers = (
            (self.theme.wall_color, wall_width, wall_width // 2),
            (colors.white, highlight_width, highlight_width // 2),
        )

        for color, width, radius in layers:
            for y, line in enumerate(maze):
                for x, cell in enumerate(line):
                    pixel_x = int(offset_x + x * cell_size)
                    pixel_y = int(offset_y + y * cell_size)
                    size = int(cell_size)

                    if cell & MazeAdapter.NORTH:
                        start = (pixel_x, pixel_y)
                        end = (pixel_x + size, pixel_y)
                        self._draw_segment(
                            screen, color, start, end, width, radius
                        )

                    if cell & MazeAdapter.EAST:
                        start = (pixel_x + size, pixel_y)
                        end = (pixel_x + size, pixel_y + size)
                        self._draw_segment(
                            screen, color, start, end, width, radius
                        )

                    if cell & MazeAdapter.SOUTH:
                        start = (pixel_x, pixel_y + size)
                        end = (pixel_x + size, pixel_y + size)
                        self._draw_segment(
                            screen, color, start, end, width, radius
                        )

                    if cell & MazeAdapter.WEST:
                        start = (pixel_x, pixel_y)
                        end = (pixel_x, pixel_y + size)
                        self._draw_segment(
                            screen, color, start, end, width, radius
                        )
