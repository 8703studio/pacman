import pygame

from src.interface.theme.theme import Theme
from src.interface import colors

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class MazeRenderer:
    """Renders the maze"""

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
        self.bottom_margin = 30
        self.theme = theme

    def get_cell_size(self, maze: list[list[int]]) -> float:
        """Calculate the cell size to fit the maze in the game window."""
        rows = len(maze)
        cols = len(maze[0])
        available_width = self.width - 2 * self.margin
        available_height = (
            self.height
            - self.hud_height
            - self.margin
            - self.bottom_margin
        )
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
            + (
                self.height
                - self.hud_height
                - self.bottom_margin
                - total_height
            ) / 2
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

        if y1 == y2:
            left = min(x1, x2) - half
            rect = pygame.Rect(left, y1 - half, abs(x2 - x1) + width, width)
        else:
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
        offset_x, offset_y = self.get_cell_position(maze, 0, 0)

        blocked_cell = NORTH | EAST | SOUTH | WEST

        for y, line in enumerate(maze):
            for x, cell in enumerate(line):
                if cell != blocked_cell:
                    continue

                left = round(offset_x + x * cell_size)
                top = round(offset_y + y * cell_size)
                right = round(offset_x + (x + 1) * cell_size)
                bottom = round(offset_y + (y + 1) * cell_size)

                pygame.draw.rect(
                    screen,
                    colors.white,
                    pygame.Rect(
                        left,
                        top,
                        right - left,
                        bottom - top,
                    ),
                )

        wall_width = max(2, int(cell_size * 0.28))
        highlight_width = max(1, int(cell_size * 0.08))

        layers = (
            (self.theme.wall_color, wall_width, wall_width // 2),
            (colors.white, highlight_width, highlight_width // 2),
        )

        for color, width, radius in layers:
            for y, line in enumerate(maze):
                for x, cell in enumerate(line):
                    left = round(offset_x + x * cell_size)
                    top = round(offset_y + y * cell_size)
                    right = round(offset_x + (x + 1) * cell_size)
                    bottom = round(offset_y + (y + 1) * cell_size)

                    blocked = cell == blocked_cell

                    if cell & NORTH:
                        if not (
                            blocked
                            and y > 0
                            and maze[y - 1][x] == blocked_cell
                        ):
                            self._draw_segment(
                                screen, color,
                                (left, top), (right, top),
                                width, radius,
                            )

                    if cell & EAST:
                        if not (
                            blocked
                            and x < cols - 1
                            and maze[y][x + 1] == blocked_cell
                        ):
                            self._draw_segment(
                                screen, color,
                                (right, top), (right, bottom),
                                width, radius,
                            )

                    if cell & SOUTH:
                        if not (
                            blocked
                            and y < rows - 1
                            and maze[y + 1][x] == blocked_cell
                        ):
                            self._draw_segment(
                                screen, color,
                                (left, bottom), (right, bottom),
                                width, radius,
                            )

                    if cell & WEST:
                        if not (
                            blocked
                            and x > 0
                            and maze[y][x - 1] == blocked_cell
                        ):
                            self._draw_segment(
                                screen, color,
                                (left, top), (left, bottom),
                                width, radius,
                            )
