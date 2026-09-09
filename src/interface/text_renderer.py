import pygame


def draw_text(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    font: pygame.font.Font,
    color: pygame.Color
) -> None:
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))
