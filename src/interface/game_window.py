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

    def draw_maze(self, maze):
        height = len(maze)
        width = len(maze[0])
        hud_height = 130
        cell_width = self.width / width
        cell_height = (self.height - hud_height) / height

        for y, line in enumerate(maze):
            for x, _ in enumerate(line):
                cell = maze[y][x]
                pixel_x = x * cell_width
                pixel_y = hud_height + y * cell_height

                if cell & MazeAdapter.NORTH:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x, pixel_y),
                        (pixel_x + cell_width, pixel_y)
                        )

                if cell & MazeAdapter.EAST:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x + cell_width, pixel_y),
                        (pixel_x + cell_width, pixel_y + cell_height)
                        )

                if cell & MazeAdapter.SOUTH:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x, pixel_y + cell_height),
                        (pixel_x + cell_width, pixel_y + cell_height)
                        )

                if cell & MazeAdapter.WEST:
                    pygame.draw.line(
                        self.screen,
                        colors.orange,
                        (pixel_x, pixel_y),
                        (pixel_x, pixel_y + cell_height)
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
