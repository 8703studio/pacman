from collections import deque
from .ghost import Ghost
from ..enums import EntityType, EntityDirection
from ..engine import Engine


class GhostChaser(Ghost):
    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.entity_type = EntityType.GHOST
        self.engine = engine

    def normal_move(self) -> None:
        engine = self.engine
        if engine is None or self.queue or self.target is None:
            return

        start = self.current_pos
        parents: dict[
            tuple[int, int], tuple[int, int] | None
        ] = {start: None}
        waiting_list = deque([start])

        while waiting_list and self.target not in parents:
            current = waiting_list.popleft()

            for direction in engine.get_valid_position(current):
                dy, dx = direction.value
                neighbour = (current[0] + dy, current[1] + dx)

                if neighbour in parents:
                    continue

                parents[neighbour] = current
                waiting_list.append(neighbour)

                if neighbour == self.target:
                    break

        if self.target not in parents:
            return

        path: list[EntityDirection] = []
        current = self.target

        while current != start:
            previous = parents[current]
            if previous is None:
                return

            vector = (
                current[0] - previous[0],
                current[1] - previous[1],
            )

            for direction in EntityDirection:
                if direction.value == vector:
                    path.append(direction)
                    break

            current = previous

        path.reverse()
        self.queue.extend(path)
        self.visited = set(parents)

    def reset(self) -> None:
        super().reset()
