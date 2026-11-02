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


def find_path(
    engine: Engine,
    ghost_position: tuple[int, int],
    target: tuple[int, int],
    blocked_positions: set[tuple[int, int]] | None = None,
) -> list[EntityDirection]:
    """Find the shortest path while avoiding occupied ghost positions."""
    if blocked_positions is None:
        blocked_positions = set()

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

            if neighbor in blocked_positions:
                continue

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
        self.other_ghosts: list[Ghost] = []
        self.pacman_position: Optional[tuple[int, int]] = None
        self.pacman_direction: Optional[EntityDirection] = None

        self.direction_queue: deque[EntityDirection] = deque()
        self.last_state = self.state

    def move(self) -> None:
        """Clear the old path on state change, then use Ghost.move()."""
        self._handle_state_change()
        super().move()

    def _blocked_positions(self) -> set[tuple[int, int]]:
        """Positions occupied by the other living ghosts."""
        return {
            ghost.current_pos
            for ghost in self.other_ghosts
            if ghost is not self
            and ghost.state != EntityState.DEAD
        }

    def normal_move(self) -> None:
        """Intercept Pacman by targeting three cell ahead."""
        engine = self.engine
        pacman_position = self.target or self.pacman_position

        if engine is None or pacman_position is None:
            return

        pacman_direction = self.pacman_direction
        if pacman_direction is None:
            target = pacman_position
        else:
            target = get_target(engine, pacman_position, pacman_direction)

        path_to_pacman = find_path(engine, self.current_pos, pacman_position)

        if path_to_pacman and len(path_to_pacman) <= 3:
            target = pacman_position

        self._queue_direction_to(target)

    def _handle_state_change(self) -> None:
        """Clear movement data when the ghost changes state."""
        if self.state == self.last_state:
            return

        self.queue.clear()
        self.direction_queue.clear()
        self.visited.clear()
        self.last_state = self.state

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
            self._blocked_positions(),
        )

        if not path and self.current_pos != target:
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

    def dead_move(self) -> None:
        """Return to the starting position while avoiding other ghosts."""
        if self.engine is None:
            return

        if self.current_pos == self.start_pos:
            self.queue.clear()
            self.direction_queue.clear()
            self.visited.clear()
            self.state = EntityState.NORMAL
            self.target = None
            self.last_state = self.state
            return

        if self.queue:
            return

        path = find_path(
            self.engine,
            self.current_pos,
            self.start_pos,
            self._blocked_positions(),
        )

        if not path:
            path = find_path(
                self.engine,
                self.current_pos,
                self.start_pos,
            )

        if not path:
            return

        self.direction_queue.extend(path)
        self.queue.extend(path)

    def reset(self) -> None:
        """Reset custom movement data and preserve dead-state handling."""
        previous_dir = self.last_dir
        previous_move = self.last_move
        super().reset()
        self.last_dir = previous_dir
        self.last_move = previous_move

        self.direction_queue.clear()
        self.pacman_position = None
        self.pacman_direction = None

        if self.state == EntityState.DEAD:
            self.last_state = self.state
            return

        self.state = EntityState.NORMAL
        self.last_state = self.state
