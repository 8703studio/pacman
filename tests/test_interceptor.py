"""INTERCEPTOR TEST"""

from typing import List, Optional
from collections import deque

pattern_test: List[List[int]] = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]


pacman_position = (1, 6)
pacman_direction = (0, 1)
ghost_position = (5, 2)


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
        next_position = (next_y, next_x)

        if grid[next_y][next_x] == 0:
            neighbors.append(next_position)

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

        neighbors = get_neighbors(grid, current)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

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


def main() -> None:
    """Run the interceptor test."""
    print("Test grid:")

    for row in pattern_test:
        print(row)

    print("Pacman:", pacman_position)
    print("Direction:", pacman_direction)
    print("Ghost:", ghost_position)

    target = get_target(
        pattern_test,
        pacman_position,
        pacman_direction,
    )

    print("Target:", target)

    neighbors = get_neighbors(
        pattern_test,
        ghost_position,
    )

    print("Neighbors:", neighbors)

    path = find_path(
        pattern_test,
        ghost_position,
        target,
    )

    print("Path:", path)

    for i in range(len(path) - 1):
        current = path[i]
        next_position = path[i + 1]

        direction = get_direction(
            current,
            next_position,
        )

        print("Ghost move:", next_position)
        print("Direction:", direction)


if __name__ == "__main__":
    main()
