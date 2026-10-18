import pygame
import mazegenerator as maze

from src.entities.entity import Entity, EntityDirection
from src.interface.renderers.entity_renderer import EntityRenderer
from src.interface.renderers.maze_renderer import MazeRenderer
from src.interface.theme.theme import CLASSIC_THEME


class PreviewGhost(Entity):
    """Temporary entity used to test ghost rendering."""

    def __init__(
        self,
        position: tuple[int, int],
        direction: EntityDirection,
    ) -> None:
        """Initialize the preview ghost."""
        super().__init__()
        self.current_pos = position
        self.direction = direction

    def move(self) -> None:
        """Keep the preview ghost stationary."""
        pass


pygame.init()

screen = pygame.display.set_mode((1024, 1080))
pygame.display.set_caption("Test Ghost Renderers")

mazegen = maze.MazeGenerator(
    (21, 21),
    seed=42,
    perfect=False,
    entry_cell=(10, 10),
)

game_maze = mazegen.maze

maze_renderer = MazeRenderer(
    width=1024,
    height=1080,
    hud_height=130,
    theme=CLASSIC_THEME,
    margin=5,
)

entity_renderer = EntityRenderer(maze_renderer)

joy = PreviewGhost((10, 6), EntityDirection.RIGHT)
gdragon = PreviewGhost((10, 9), EntityDirection.LEFT)
momo = PreviewGhost((10, 12), EntityDirection.UP)
louis = PreviewGhost((10, 15), EntityDirection.DOWN)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    maze_renderer.draw(screen, game_maze)

    entity_renderer.draw_joy(screen, game_maze, joy)
    entity_renderer.draw_gdragon(screen, game_maze, gdragon)
    entity_renderer.draw_momo(screen, game_maze, momo)
    entity_renderer.draw_louis(screen, game_maze, louis)

    pygame.display.flip()

pygame.quit()
