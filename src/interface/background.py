"""Functions for drawing themed backgrounds."""

from functools import lru_cache

import pygame


@lru_cache(maxsize=16)
def load_background(
    image_path: str,
    size: tuple[int, int],
) -> pygame.Surface:
    """Load and scale a background image, caching the result."""

    image = pygame.image.load(image_path).convert()
    return pygame.transform.scale(image, size)


def draw_background(
    screen: pygame.Surface,
    background_color: pygame.Color,
    image_path: str | None,
) -> None:
    """Draw an image background or a solid color."""

    if image_path is None:
        screen.fill(background_color)
        return

    background = load_background(
        image_path,
        screen.get_size(),
    )
    screen.blit(background, (0, 0))
