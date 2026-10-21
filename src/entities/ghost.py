from .entity import Entity
from abc import ABC, abstractmethod
from ..enums import EntityDirection, EntityState
from ..engine import Engine
from time import monotonic
from collections import deque
import random


class Ghost(Entity, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.speed = 1
        self.engine: Engine | None = None
        self.target: tuple[int, int] | None = None
        self.neighboor = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
        ]

    def move(self) -> None:
        if self.state == EntityState.NORMAL:
            self.normal_move()
        elif self.state == EntityState.WEAK:
            self.weak_move()
        elif self.state == EntityState.DEAD:
            self.dead_move()

    @abstractmethod
    def normal_move(self) -> None:
        pass

    def weak_move(self) -> None:
        """Run away from Pacman while vulnerable."""
        engine = self.engine
        target = self.target
        if engine is None or target is None or self.queue:
            return

        valid_directions = engine.get_valid_position(self.current_pos)
        if not valid_directions:
            return

        if self.last_dir is not None:
            back = (-self.last_dir.value[0], -self.last_dir.value[1])
            forward = [d for d in valid_directions if d.value != back]
            if forward:
                valid_directions = forward

        distances: dict[tuple[int, int], int] = {target: 0}
        waiting_list = deque([target])

        while waiting_list:
            current = waiting_list.popleft()

            for direction in engine.get_valid_position(current):
                dy, dx = direction.value
                neighbour = (current[0] + dy, current[1] + dx)

                if neighbour in distances:
                    continue

                distances[neighbour] = distances[current] + 1
                waiting_list.append(neighbour)

        cy, cx = self.current_pos
        score = {
            direction: distances.get(
                (cy + direction.value[0], cx + direction.value[1]), 0
            )
            for direction in valid_directions
        }
        farthest = max(score.values())
        self.queue.append(
            random.choice(
                [d for d in valid_directions if score[d] == farthest]
            )
        )

    def dead_move(self) -> None:
        """Return to the starting position when eaten."""
        engine = self.engine
        if engine is None:
            return

        if self.current_pos == self.start_pos:
            self.queue.clear()
            self.visited.clear()
            self.state = EntityState.NORMAL
            self.target = None
            return

        if self.queue:
            return

        start = self.current_pos
        parents: dict[
            tuple[int, int],
            tuple[tuple[int, int], EntityDirection] | None,
        ] = {start: None}
        waiting_list = deque([start])

        while waiting_list and self.start_pos not in parents:
            current = waiting_list.popleft()

            for direction in engine.get_valid_position(current):
                dy, dx = direction.value
                neighbour = (current[0] + dy, current[1] + dx)

                if neighbour in parents:
                    continue

                parents[neighbour] = (current, direction)
                waiting_list.append(neighbour)

        if self.start_pos not in parents:
            return

        path: list[EntityDirection] = []
        current = self.start_pos

        while current != start:
            parent = parents[current]
            if parent is None:
                return

            previous, direction = parent
            path.append(direction)
            current = previous

        self.queue.extend(reversed(path))

    def reset(self) -> None:
        super().reset()
        self.last_move = monotonic()
        self.last_dir = None
