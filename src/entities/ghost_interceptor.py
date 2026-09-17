from src.entities.entity import (
    Entity,
    EntityType,
    EntityState,
    EntityDirection,
)

from collections import deque
from typing import Optional
from src.maze.maze_adapter import MazeAdapter


def get_target(
    grid: list[list[int]],
    pacman_position: tuple[int, int],
    pacman_direction: tuple[int, int],
) -> tuple[int, int]:
    """Find the interception target."""
    position = pacman_position

    for _ in range(3):
        next_y = position[0] + pacman_direction[0]
        next_x = position[1] + pacman_direction[1]
        next_position = (next_y, next_x)

        if grid[next_y][next_x] == 1:
            break

        position = next_position

    return position


def get_neighbors(
    grid: list[list[int]],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return accessible neighboring positions."""
    neighbors = []

    directions = [
        (-1, 0),
        (1, 0),
        (0, 1),
        (0, -1),
    ]

    for direction in directions:
        next_y = position[0] + direction[0]
        next_x = position[1] + direction[1]

        if grid[next_y][next_x] == 0:
            neighbors.append((next_y, next_x))

    return neighbors


def find_path(
    grid: list[list[int]],
    ghost_position: tuple[int, int],
    target: tuple[int, int],
) -> list[tuple[int, int]]:
    """Find a path from the ghost to the target."""
    queue = deque([ghost_position])
    visited = {ghost_position}

    came_from: dict[tuple[int, int], Optional[tuple[int, int]]] = {
        ghost_position: None
    }

    while queue:
        current = queue.popleft()

        if current == target:
            break

        for neighbor in get_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    if target not in came_from:
        return []

    path = []
    current = target

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path


def get_direction(
    current: tuple[int, int],
    next_position: tuple[int, int],
) -> tuple[int, int]:
    """Return the direction between two positions."""
    current_y, current_x = current
    next_y, next_x = next_position

    if current_y == next_y and next_x < current_x:
        return (0, -1)

    if current_y == next_y and next_x > current_x:
        return (0, 1)

    if current_x == next_x and next_y < current_y:
        return (-1, 0)

    if current_x == next_x and next_y > current_y:
        return (1, 0)

    return (0, 0)


class Ghost_interceptor(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.entity_type = EntityType.GHOST
        self.grid: Optional[list[list[int]]] = None
        self.pacman_position: Optional[tuple[int, int]] = None
        self.pacman_direction: Optional[tuple[int, int]] = None

    def move(self) -> None:
        if (
            self.grid is None
            or self.pacman_position is None
            or self.pacman_direction is None
        ):
            return

        target = get_target(
            self.grid,
            self.pacman_position,
            self.pacman_direction,
        )

        path = find_path(
            self.grid,
            self.current_pos,
            target,
        )

        if len(path) > 1:
            next_position = path[1]

            direction = get_direction(
                self.current_pos,
                next_position,
            )

            self.direction = EntityDirection(direction)
            self.current_pos = next_position

    def reset(self):
        return super().reset()
