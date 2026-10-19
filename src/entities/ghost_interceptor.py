from collections import deque
from typing import Optional

from src.entities.entity import (
    Entity,
    EntityType,
    EntityDirection,
    EntityState,
)
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
        if not engine.is_valid_position(direction, position):
            break
        position = (
            position[0] + direction[0],
            position[1] + direction[1],
        )

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


def get_distance_map(
    engine: Engine,
    start: tuple[int, int],
) -> dict[tuple[int, int], int]:
    """Return the shortest distance from start to each reachable cell."""
    waiting = deque([start])
    distances = {start: 0}

    while waiting:
        current = waiting.popleft()

        for neighbor in get_neighbors(engine, current):
            if neighbor in distances:
                continue

            distances[neighbor] = distances[current] + 1
            waiting.append(neighbor)

    return distances


def get_center_target(
    engine: Engine,
    start: tuple[int, int],
) -> tuple[int, int]:
    """Find the reachable cell closest to the maze center."""
    distances = get_distance_map(engine, start)
    rows = len(engine.grid)

    if rows == 0:
        return start

    columns = len(engine.grid[0])

    if columns == 0:
        return start

    center = (rows // 2, columns // 2)

    return min(
        distances,
        key=lambda cell: (
            abs(cell[0] - center[0])
            + abs(cell[1] - center[1]),
            distances[cell],
        ),
    )


def get_weak_target(
    engine: Engine,
    ghost_position: tuple[int, int],
    pacman_position: tuple[int, int],
    last_direction: Optional[EntityDirection],
    recent_positions: set[tuple[int, int]],
) -> Optional[tuple[int, int]]:
    """Choose a distant neighboring cell while avoiding recent positions."""
    neighbors = get_neighbors(engine, ghost_position)

    if not neighbors:
        return None

    fresh_neighbors = [
        neighbor
        for neighbor in neighbors
        if neighbor not in recent_positions
    ]

    if fresh_neighbors:
        neighbors = fresh_neighbors
    elif last_direction is not None and len(neighbors) > 1:
        dy, dx = last_direction.value
        previous = (
            ghost_position[0] - dy,
            ghost_position[1] - dx,
        )
        alternatives = [
            neighbor
            for neighbor in neighbors
            if neighbor != previous
        ]

        if alternatives:
            neighbors = alternatives

    distances = get_distance_map(engine, pacman_position)
    rows = len(engine.grid)
    columns = len(engine.grid[0]) if rows else 0
    unreachable_distance = rows * columns + 1

    return max(
        neighbors,
        key=lambda cell: distances.get(cell, unreachable_distance),
    )


def find_path(
    engine: Engine,
    ghost_position: tuple[int, int],
    target: tuple[int, int],
) -> list[tuple[int, int]]:
    """Find a path from the ghost to the target."""
    waiting = deque([ghost_position])
    visited = {ghost_position}
    came_from: dict[
        tuple[int, int],
        Optional[tuple[int, int]],
    ] = {ghost_position: None}

    while waiting:
        current = waiting.popleft()

        if current == target:
            break

        for neighbor in get_neighbors(engine, current):
            if neighbor in visited:
                continue

            visited.add(neighbor)
            came_from[neighbor] = current
            waiting.append(neighbor)

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
        direction = get_direction(path[index], path[index + 1])
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


class GhostInterceptor(Entity):
    """Ghost that intercepts Pacman and handles weak/dead behavior."""

    def __init__(self, position: tuple[int, int]) -> None:
        """Initialize the interceptor ghost at its starting position."""
        super().__init__()
        self.start_pos = position
        self.current_pos = position
        self.entity_type = EntityType.GHOST

        self.engine: Optional[Engine] = None
        self.pacman_position: Optional[tuple[int, int]] = None
        self.pacman_direction: Optional[EntityDirection] = None
        self.last_pacman_direction: Optional[EntityDirection] = None

        self.direction_queue: deque[tuple[int, int]] = deque()
        self.weak_history: deque[tuple[int, int]] = deque(maxlen=8)
        self.move_timer = 0

        self.last_state = self.state
        self.dead_phase = "center"
        self.dead_center: Optional[tuple[int, int]] = None

    def move(self) -> None:
        """Choose the next move according to the ghost state."""
        self._handle_state_change()

        engine = self.engine
        if engine is None:
            return

        if self.state not in (
            EntityState.NORMAL,
            EntityState.WEAK,
            EntityState.DEAD,
        ):
            return

        self.move_timer += 1

        if self.move_timer < 10:
            return

        self.move_timer = 0

        if self.state == EntityState.NORMAL:
            pacman_position = self.pacman_position
            pacman_direction = self.pacman_direction

            if pacman_position is None or pacman_direction is None:
                return

            target = get_target(
                engine,
                pacman_position,
                pacman_direction,
            )

        elif self.state == EntityState.WEAK:
            pacman_position = self.pacman_position

            if pacman_position is None:
                return

            if not self.weak_history or (
                self.weak_history[-1] != self.current_pos
            ):
                self.weak_history.append(self.current_pos)

            target = get_weak_target(
                engine,
                self.current_pos,
                pacman_position,
                self.last_dir,
                set(self.weak_history),
            )

            if target is None:
                return

        else:
            target = self._get_dead_target()

            if target is None:
                return

        self._queue_direction_to(target)

    def _handle_state_change(self) -> None:
        """Clear movement data when the ghost changes state."""
        if self.state == self.last_state:
            return

        self.direction_queue.clear()
        self.queue.clear()
        self.weak_history.clear()

        if self.state == EntityState.WEAK:
            self.weak_history.append(self.current_pos)
        self.move_timer = 0

        if self.state == EntityState.DEAD:
            self.dead_phase = "center"
            self.dead_center = None

        self.last_state = self.state

    def _get_dead_target(
        self,
    ) -> Optional[tuple[int, int]]:
        """Return the center target, then the spawn position."""
        if self.engine is None:
            return None

        if self.dead_center is None:
            self.dead_center = get_center_target(
                self.engine,
                self.current_pos,
            )

        if (
            self.dead_phase == "center"
            and self.current_pos == self.dead_center
        ):
            self.dead_phase = "spawn"

        if (
            self.dead_phase == "spawn"
            and self.current_pos == self.start_pos
        ):
            self.state = EntityState.NORMAL
            self.direction_queue.clear()
            self.queue.clear()
            return None

        if self.dead_phase == "center":
            return self.dead_center

        return self.start_pos

    def _queue_direction_to(
        self,
        target: tuple[int, int],
    ) -> None:
        """Queue the first direction of the path to a target."""
        if self.engine is None:
            return

        path = find_path(self.engine, self.current_pos, target)

        self.direction_queue.clear()
        self.direction_queue.extend(path)
        self.queue.clear()

        if not self.direction_queue:
            return

        direction = self.direction_queue.popleft()
        entity_direction = EntityDirection(direction)
        self.direction = entity_direction
        self.queue.append(entity_direction)

    def update_ghost(self) -> None:
        """Update the ghost state."""
        pass

    def reset(self) -> None:
        """Clear movement data and reset when the ghost is not dead."""
        self.direction_queue.clear()
        self.queue.clear()
        self.move_timer = 0
        self.last_dir = None

        if self.state == EntityState.DEAD:
            self.dead_phase = "center"
            self.dead_center = None
            self.last_state = self.state
            return

        self.current_pos = self.start_pos
        self.state = EntityState.NORMAL
        self.last_state = self.state
        self.dead_phase = "center"
        self.dead_center = None
