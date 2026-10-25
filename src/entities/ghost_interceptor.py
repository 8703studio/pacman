
from collections import deque
from typing import Optional

from ..enums import EntityType, EntityDirection, EntityState
from ..engine import Engine
from .ghost import Ghost


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
        if engine.is_valid_position(direction, position):
            neighbors.append(
                (
                    position[0] + direction[0],
                    position[1] + direction[1],
                )
            )

    return neighbors


def get_distance_map(
    engine: Engine,
    start: tuple[int, int],
) -> dict[tuple[int, int], int]:
    """Return shortest distances from the starting cell."""
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

    if not engine.grid or not engine.grid[0]:
        return start

    center = (
        len(engine.grid) // 2,
        len(engine.grid[0]) // 2,
    )

    return min(
        distances,
        key=lambda cell: (
            abs(cell[0] - center[0]) + abs(cell[1] - center[1]),
            distances[cell],
        ),
    )


def get_weak_target(
    engine: Engine,
    ghost_position: tuple[int, int],
    pacman_position: tuple[int, int],
    recent_positions: set[tuple[int, int]],
) -> Optional[tuple[int, int]]:
    """Choose a distant destination and avoid recent positions."""
    pacman_distances = get_distance_map(engine, pacman_position)
    ghost_distances = get_distance_map(engine, ghost_position)

    candidates = [
        cell
        for cell in ghost_distances
        if cell != ghost_position
        and cell not in recent_positions
        and len(get_neighbors(engine, cell)) >= 2
    ]

    if not candidates:
        candidates = [
            cell
            for cell in ghost_distances
            if cell != ghost_position and cell not in recent_positions
        ]

    if not candidates:
        candidates = [
            cell for cell in ghost_distances if cell != ghost_position
        ]

    if not candidates:
        return None

    return max(
        candidates,
        key=lambda cell: (
            pacman_distances.get(cell, -1),
            len(get_neighbors(engine, cell)),
            ghost_distances[cell],
        ),
    )


def find_path(
    engine: Engine,
    ghost_position: tuple[int, int],
    target: tuple[int, int],
) -> list[EntityDirection]:
    """Find the shortest sequence of directions to a target."""
    waiting = deque([ghost_position])
    came_from: dict[
        tuple[int, int],
        Optional[tuple[tuple[int, int], EntityDirection]],
    ] = {ghost_position: None}

    while waiting:
        current = waiting.popleft()

        if current == target:
            break

        for direction in engine.get_valid_position(current):
            dy, dx = direction.value
            neighbor = (current[0] + dy, current[1] + dx)

            if neighbor in came_from:
                continue

            came_from[neighbor] = (current, direction)
            waiting.append(neighbor)

    if target not in came_from:
        return []

    path = []
    current = target

    while current != ghost_position:
        parent = came_from[current]

        if parent is None:
            return []

        previous, direction = parent
        path.append(direction)
        current = previous

    path.reverse()
    return path


class GhostInterceptor(Ghost):
    """Ghost that intercepts Pacman and preserves custom weak/dead behavior."""

    def __init__(
        self,
        position: tuple[int, int],
        engine: Engine | None = None,
    ) -> None:
        super().__init__()

        self.start_pos = position
        self.current_pos = position
        self.entity_type = EntityType.GHOST
        self.engine = engine

        self.pacman_position: Optional[tuple[int, int]] = None
        self.pacman_direction: Optional[EntityDirection] = None

        self.direction_queue: deque[EntityDirection] = deque()
        self.weak_history: deque[tuple[int, int]] = deque(maxlen=8)
        self.weak_target: Optional[tuple[int, int]] = None

        self.last_state = self.state
        self.dead_phase = "center"
        self.dead_center: Optional[tuple[int, int]] = None

    def normal_move(self) -> None:
        """Intercept Pacman by targeting three cells ahead."""
        engine = self.engine
        pacman_position = self.target or self.pacman_position
        pacman_direction = self.pacman_direction

        if engine is None or pacman_position is None:
            return

        if pacman_direction is None:
            target = pacman_position
        else:
            target = get_target(
                engine,
                pacman_position,
                pacman_direction,
            )

        self._queue_direction_to(target)

    # def weak_move(self) -> None:
    #     """Run away from Pacman using the original weak-state strategy."""
    #     self._handle_state_change()

    #     engine = self.engine
    #     pacman_position = self.target or self.pacman_position

    #     if engine is None or pacman_position is None:
    #         return

    #     if not self.weak_history or self.weak_history[-1] != self.current_pos:
    #         self.weak_history.append(self.current_pos)

    #     if self.weak_target is None or self.current_pos == self.weak_target:
    #         self.weak_target = get_weak_target(
    #             engine,
    #             self.current_pos,
    #             pacman_position,
    #             set(self.weak_history),
    #         )

    #     if self.weak_target is not None:
    #         self._queue_direction_to(self.weak_target)

    # def dead_move(self) -> None:
    #     """Return to the maze center, then the starting position."""
    #     self._handle_state_change()

    #     target = self._get_dead_target()

    #     if target is not None:
    #         self._queue_direction_to(target)

    def _handle_state_change(self) -> None:
        """Clear movement data when the ghost changes state."""
        if self.state == self.last_state:
            return

        self.queue.clear()
        self.direction_queue.clear()
        self.visited.clear()
        self.weak_history.clear()
        self.weak_target = None

        if self.state == EntityState.WEAK:
            self.weak_history.append(self.current_pos)

        if self.state == EntityState.DEAD:
            self.dead_phase = "center"
            self.dead_center = None

        self.last_state = self.state

    def _get_dead_target(self) -> Optional[tuple[int, int]]:
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

        if self.dead_phase == "spawn" and self.current_pos == self.start_pos:
            self.queue.clear()
            self.direction_queue.clear()
            self.weak_target = None
            self.state = EntityState.NORMAL
            self.last_state = self.state
            self.dead_phase = "center"
            self.dead_center = None
            return None

        if self.dead_phase == "center":
            return self.dead_center

        return self.start_pos

    def _queue_direction_to(
        self,
        target: tuple[int, int],
    ) -> None:
        """Queue the path directions using Entity's movement queue."""
        if self.engine is None:
            return

        path = find_path(
            self.engine,
            self.current_pos,
            target,
        )

        self.queue.clear()
        self.direction_queue.clear()

        if not path:
            return

        self.direction_queue.extend(path)
        self.queue.extend(path)

    def reset(self) -> None:
        """Reset custom movement data and preserve dead-state handling."""
        super().reset()

        self.direction_queue.clear()
        self.weak_history.clear()
        self.weak_target = None
        self.pacman_position = None
        self.pacman_direction = None

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
