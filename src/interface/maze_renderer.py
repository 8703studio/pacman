import pygame

from src.maze.maze_adapter import MazeAdapter
from src.interface import colors


class MazeRenderer:
    def __init__(self, width, height, hud_height=130, margin=5):
        self.width = width
        self.height = height
        self.hud_height = hud_height
        self.margin = margin

    def get_cell_size(self, maze):
        rows = len(maze)
        cols = len(maze[0])

        available_width = self.width - 2 * self.margin
        available_height = (
            self.height
            - self.hud_height
            - 2 * self.margin
        )

        cell_size = min(
            available_width / cols,
            available_height / rows
        )

        return cell_size

    def draw(self, screen, maze):
        rows = len(maze)
        cols = len(maze[0])

        cell_size = self.get_cell_size(maze)

        total_width = cell_size * cols
        total_height = cell_size * rows

        offset_x = (
            (self.width - total_width) / 2
            + self.margin
        )

        offset_y = (
            self.hud_height
            + (
                self.height
                - self.hud_height
                - total_height
            ) / 2
            + self.margin
        )

        for y, line in enumerate(maze):
            for x, cell in enumerate(line):
                pixel_x = int(offset_x + x * cell_size)
                pixel_y = int(offset_y + y * cell_size)
                size = int(cell_size)

                if cell & MazeAdapter.NORTH:
                    pygame.draw.line(
                        screen,
                        colors.orange,
                        (pixel_x, pixel_y),
                        (pixel_x + size, pixel_y),
                        2
                    )

                if cell & MazeAdapter.EAST:
                    pygame.draw.line(
                        screen,
                        colors.orange,
                        (pixel_x + size, pixel_y),
                        (pixel_x + size, pixel_y + size),
                        2
                    )

                if cell & MazeAdapter.SOUTH:
                    pygame.draw.line(
                        screen,
                        colors.orange,
                        (pixel_x, pixel_y + size),
                        (pixel_x + size, pixel_y + size),
                        2
                    )

                if cell & MazeAdapter.WEST:
                    pygame.draw.line(
                        screen,
                        colors.orange,
                        (pixel_x, pixel_y),
                        (pixel_x, pixel_y + size),
                        2
                    )

    def draw_entities(self, screen, player, ghosts, pellets):
        pass
