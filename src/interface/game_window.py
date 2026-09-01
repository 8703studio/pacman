import pygame
from typing import Optional
from src.interface.theme.theme import CLASSIC_THEME
from src.interface.hud import HUD
from src.interface.theme.theme_manager import ThemeManager
from src.maze.maze_adapter import MazeAdapter
from src.interface import colors


class GameWindow:
    def __init__(self, width, height):
        pygame.init()

        self.theme_manager = ThemeManager(CLASSIC_THEME)
        self.running = True
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.hud = HUD()
        self.maze: Optional[list[list[int]]] = None

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pac-idol")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass

    def update(self, delta_time):
        pass

    def draw(self):
        self.screen.fill(
            self.theme_manager.get_theme().background_color
        )

        if self.maze is not None:
            self.draw_maze(self.maze)

        self.hud.render(
            self.screen,
            score=0,
            lives=3,
            level=1,
            time_left=120
            )

    def get_cell_size(self, maze):
        hud_height = 130

        rows = len(maze)
        cols = len(maze[0])

        cell_width = self.width / cols
        cell_height = (self.height - hud_height) / rows

        return cell_width, cell_height, hud_height

    def draw_maze(self, maze):
        hud_height = 130

        rows = len(maze)
        cols = len(maze[0])

        margin = 5

        available_width = self.width - 2 * margin
        available_height = self.height - hud_height - 2 * margin

        cell_size = min(
            available_width / cols,
            available_height / rows
        )

        total_width = cell_size * cols
        total_height = cell_size * rows

        offset_x = (self.width - total_width) / 2 + margin
        offset_y = hud_height + (available_height - total_height) / 2 + margin

        for y, line in enumerate(maze):
            for x, cell in enumerate(line):

                pixel_x = int(offset_x + x * cell_size)
                pixel_y = int(offset_y + y * cell_size)
                size = int(cell_size)

                if cell & MazeAdapter.NORTH:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x, pixel_y),
                        (pixel_x + size, pixel_y),
                        2
                    )

                if cell & MazeAdapter.EAST:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x + size, pixel_y),
                        (pixel_x + size, pixel_y + size),
                        2
                    )

                if cell & MazeAdapter.SOUTH:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x, pixel_y + size),
                        (pixel_x + size, pixel_y + size),
                        2
                    )

                if cell & MazeAdapter.WEST:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x, pixel_y),
                        (pixel_x, pixel_y + size),
                        2
                    )

    def draw_entities(self, player, ghosts, pellets):
        pass

    def run(self):
        while self.running:
            self.handle_events()
            delta_time = self.clock.tick(60) / 1000
            self.update(delta_time)
            self.draw()
            pygame.display.flip()
        pygame.quit()
