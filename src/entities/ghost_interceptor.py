from collections import deque

from typing import Optional

from src.entities.entity import Entity, EntityType, EntityDirection

from src.engine.physics import Engine

DIRECTION_TO_STRING = {
    EntityDirection.UP: "up",
    EntityDirection.RIGHT: "right",
    EntityDirection.DOWN: "down",
    EntityDirection.LEFT: "left",
}


def get_target(
    engine: Engine,
    pacman_position: tuple[int, int],
    pacman_direction: EntityDirection,
) -> tuple[int, int]:
    """Find the interception target three cells ahead of Pacman."""

    position = pacman_position

    direction = pacman_direction.value

    for _ in range(3):
        next_position = (
            position[0] + direction[0],
            position[1] + direction[1],
        )

        if not engine.is_valid_position(direction, position):
            break

        position = next_position

    return position


def get_neighbors(
    engine: Engine,
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return accessible neighboring positions."""

    directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]

    neighbors = []

    for direction in directions:
        next_position = (
            position[0] + direction[0],
            position[1] + direction[1],
        )

        if engine.is_valid_position(direction, position):
            neighbors.append(next_position)

    return neighbors


def find_path(
    engine: Engine,
    ghost_position: tuple[int, int],
    target: tuple[int, int],
) -> list[tuple[int, int]]:
    """Find a path from the ghost to the target."""
    queue = deque([ghost_position])

    visited = {ghost_position}

    came_from: dict[
        tuple[int, int],
        Optional[tuple[int, int]],
    ] = {ghost_position: None}

    while queue:
        current = queue.popleft()

        if current == target:
            break

        for neighbor in get_neighbors(
            engine,
            current,
        ):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    if target not in came_from:
        return []

    path = []

    walk: Optional[tuple[int, int]] = target

    while walk is not None:
        path.append(walk)
        walk = came_from[walk]

    path.reverse()

    directions = []

    for index in range(len(path) - 1):
        direction = get_direction(
            path[index],
            path[index + 1],
        )
        directions.append(direction)

    return directions


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
    """Ghost that intercepts Pacman by predicting his path with BFS."""

    def __init__(self, position: tuple[int, int]) -> None:
        """Initialize the interceptor ghost at its starting position."""
        super().__init__(position)

        self.entity_type = EntityType.GHOST

        self.engine: Optional[Engine] = None

        self.pacman_position: Optional[tuple[int, int]] = None

        self.pacman_direction: Optional[EntityDirection] = None

        self.direction_queue: deque[tuple[int, int]] = deque()

        self.move_timer = 0

    def move(self) -> tuple[int, int]:
        """Return the next direction for the ghost."""
        if (
            self.engine is None
            or self.pacman_position is None
            or self.pacman_direction is None
        ):
            return (0, 0)

        self.move_timer += 1

        if self.move_timer < 10:
            return (0, 0)

        self.move_timer = 0

        if not self.direction_queue:
            target = get_target(
                self.engine,
                self.pacman_position,
                self.pacman_direction,
            )

            path = find_path(
                self.engine,
                self.current_pos,
                target,
            )

            self.direction_queue.extend(path)

        if self.direction_queue:
            direction = self.direction_queue.popleft()
            self.direction = EntityDirection(direction)
            return direction

        return (0, 0)

    def update_ghost(self) -> None:
        """Update the ghost state."""
        pass

    def reset(self) -> None:
        """Reset the ghost to its starting position."""
        self.current_pos = self.start_pos
        self.direction_queue.clear()
        self.move_timer = 0
