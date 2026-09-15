import pygame


def draw_text(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    font: pygame.font.Font,
    color: pygame.Color,
) -> None:
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def get_center(
    screen: pygame.Surface,
) -> tuple[int, int]:
    """Center the elements"""
    return (screen.get_width() // 2, screen.get_height() // 2)
