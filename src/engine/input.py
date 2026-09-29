import pygame


def get_direction(event):
    if event.type != pygame.KEYDOWN:
        return None
    if event.key == pygame.K_UP:
        return (-1, 0)
    if event.key == pygame.K_DOWN:
        return (1, 0)
    if event.key == pygame.K_LEFT:
        return (0, -1)
    if event.key == pygame.K_RIGHT:
        return (0, 1)
    return None
