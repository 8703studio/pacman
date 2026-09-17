from collections import deque

from typing import Optional

from src.entities.entity import Entity, EntityType, EntityDirection

from src.maze.maze_adapter import MazeAdapter


DIRECTION_TO_STRING = {
    EntityDirection.UP: "up",
    EntityDirection.RIGHT: "right",
    EntityDirection.DOWN: "down",
    EntityDirection.LEFT: "left",
}


def get_target(
    maze_adapter: MazeAdapter,
    grid: list[list[int]],
    pacman_position: tuple[int, int],
    pacman_direction: EntityDirection,
) -> tuple[int, int]:
    """Find the interception target three cells ahead of Pacman."""
    direction_str = DIRECTION_TO_STRING[pacman_direction]
    position = pacman_position

    for _ in range(3):
        y, x = position

        print(
            "TEST TARGET :",
            position,
            direction_str,
            "WALL =",
            maze_adapter.is_wall(grid, x, y, direction_str),
        )

        if maze_adapter.is_wall(grid, x, y, direction_str):
            break

        next_x, next_y = maze_adapter.get_neighbor(
            x,
            y,
            direction_str,
        )

        position = (next_y, next_x)

    return position


def get_neighbors(
    maze_adapter: MazeAdapter,
    grid: list[list[int]],
    position: tuple[int, int],
) -> list[tuple[int, int]]:
    """Return accessible neighboring positions."""
    y, x = position

    neighbors = maze_adapter.get_neighbors(
        grid,
        x,
        y,
    )

    return [(next_y, next_x) for next_x, next_y in neighbors]


def find_path(
    maze_adapter: MazeAdapter,
    grid: list[list[int]],
    ghost_position: tuple[int, int],
    target: tuple[int, int],
) -> list[tuple[int, int]]:
    """Find a path from the ghost to the target."""
    queue = deque([ghost_position])

    visited = {ghost_position}

    came_from: dict[
        tuple[int, int],
        Optional[tuple[int, int]],
    ] = {
        ghost_position: None
    }

    while queue:
        current = queue.popleft()

        if current == target:
            break

        for neighbor in get_neighbors(
            maze_adapter,
            grid,
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
    """Ghost that intercepts Pacman by predicting his path with BFS."""

    def __init__(self, position: tuple[int, int]) -> None:
        """Initialize the interceptor ghost at its starting position."""
        super().__init__(position)

        self.entity_type = EntityType.GHOST

        self.maze_adapter = MazeAdapter()

        self.grid: Optional[list[list[int]]] = None

        self.pacman_position: Optional[tuple[int, int]] = None

        self.pacman_direction: Optional[EntityDirection] = None

        self.move_timer = 0

    def move(
        self,
        direction=None,
    ) -> None:
        """Move the ghost one step along the path towards its target."""
        if (
            self.grid is None
            or self.pacman_position is None
            or self.pacman_direction is None
        ):
            return

        self.move_timer += 1

        if self.move_timer < 10:
            return

        self.move_timer = 0

        print("PACMAN :", self.pacman_position)

        print("DIRECTION PACMAN :", self.pacman_direction)

        target = get_target(
            self.maze_adapter,
            self.grid,
            self.pacman_position,
            self.pacman_direction,
        )

        print("POSITION PACMAN :", self.pacman_position)

        print("TARGET CALCULE :", target)

        path = find_path(
            self.maze_adapter,
            self.grid,
            self.current_pos,
            target,
        )

        print("FANTOME :", self.current_pos)

        print("TARGET :", target)

        print("PATH :", path)

        if len(path) > 1:
            next_position = path[1]

            direction = get_direction(
                self.current_pos,
                next_position,
            )

            self.direction = EntityDirection(direction)

            self.current_pos = next_position

    def reset(self) -> None:
        """Reset the ghost to its starting position."""
        self.current_pos = self.start_pos
