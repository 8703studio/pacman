import random
from pathlib import Path

import pygame

from src.enums.grid_object import GridObject
from src.interface.renderers.maze_renderer import MazeRenderer


class ObjectRenderer:
    """Render gums, supergums and lightsticks on the maze grid."""

    def __init__(self, maze_renderer: MazeRenderer) -> None:
        """Initialize the object renderer and load its assets."""
        self.maze_renderer = maze_renderer

        assets_dir = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "game"
        )

        lightsticks_dir = (
            Path(__file__).resolve().parent.parent
            / "assets"
            / "lighstick"
        )

        self.gum_image = pygame.image.load(
            str(assets_dir / "hearrtspacgum.png")
        ).convert_alpha()

        self.supergum_image = pygame.image.load(
            str(assets_dir / "superpacgum.png")
        ).convert_alpha()

        self.lightstick_images = [
            pygame.image.load(str(path)).convert_alpha()
            for path in sorted(lightsticks_dir.glob("*.png"))
        ]

        self.fruit_lightsticks: dict[
            tuple[int, int], pygame.Surface
        ] = {}

        self.scaled_images: dict[
            tuple[GridObject, int, str], pygame.Surface
        ] = {}

    def _get_image(
        self,
        obj: GridObject,
        cell_size: float,
    ) -> pygame.Surface | None:
        """Return the appropriately scaled image for an object."""
        if obj == GridObject.GUM:
            image = self.gum_image
            scale = 0.25
            asset_key = "gum"
        elif obj == GridObject.SUPERGUM:
            image = self.supergum_image
            scale = 0.55
            asset_key = "supergum"
        else:
            return None

        size = max(2, int(cell_size * scale))
        key = (obj, size, asset_key)

        if key not in self.scaled_images:
            self.scaled_images[key] = pygame.transform.smoothscale(
                image,
                (size, size),
            )

        return self.scaled_images[key]

    def draw(
        self,
        screen: pygame.Surface,
        maze: list[list[int]],
        grid_objects: list[list[GridObject]],
    ) -> None:
        """Draw collectible objects at their corresponding grid cells."""
        cell_size = self.maze_renderer.get_cell_size(maze)
        visible_fruits: set[tuple[int, int]] = set()

        for y, row in enumerate(grid_objects):
            for x, obj in enumerate(row):
                if obj == GridObject.FRUIT:
                    position = (x, y)
                    visible_fruits.add(position)

                    if position not in self.fruit_lightsticks:
                        if not self.lightstick_images:
                            continue

                        self.fruit_lightsticks[position] = (
                            random.choice(self.lightstick_images)
                        )

                    fruit_image = self.fruit_lightsticks[position]
                    size = max(2, int(cell_size * 0.55))
                    key = (obj, size, str(fruit_image))

                    if key not in self.scaled_images:
                        self.scaled_images[key] = (
                            pygame.transform.smoothscale(
                                fruit_image,
                                (size, size),
                            )
                        )

                    draw_image = self.scaled_images[key]
                else:
                    object_image = self._get_image(obj, cell_size)

                    if object_image is None:
                        continue

                    draw_image = object_image

                cell_x, cell_y = self.maze_renderer.get_cell_position(
                    maze, x, y
                )

                rect = draw_image.get_rect(
                    center=(
                        round(cell_x + cell_size / 2),
                        round(cell_y + cell_size / 2),
                    )
                )

                screen.blit(draw_image, rect)

        self.fruit_lightsticks = {
            position: image
            for position, image in self.fruit_lightsticks.items()
            if position in visible_fruits
        }
