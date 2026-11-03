from time import monotonic
from ...entities.entity import Entity


class EntityAnimator:
    def __init__(self) -> None:
        self.prev = {}
        self.start = {}

    def pos(self, entity: Entity) -> tuple[int, int]:
        cur = entity.current_pos
        prev, last = self.prev.get(id(entity), (cur, cur))
        if cur != last:
            prev = last
            self.start[id(entity)] = entity.last_move
        self.prev[id(entity)] = (prev, cur)
        if entity.speed <= 0:
            return cur
        started = self.start.get(id(entity), entity.last_move)
        t = min(1.0, (monotonic() - started) / entity.speed)
        return (prev[0] + (cur[0] - prev[0]) * t,
                prev[1] + (cur[1] - prev[1]) * t)

    def progress(self, entity: Entity):
        if entity.speed <= 0:
            return 1.0

        started = self.start.get(id(entity), entity.last_move)
        return min(1.0, (monotonic() - started) / entity.speed)
