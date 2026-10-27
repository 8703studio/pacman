from time import monotonic


class EntityAnimator:
    def __init__(self):
        self.prev = {}

    def pos(self, entity):
        cur = entity.current_pos
        prev, last = self.prev.get(id(entity), (cur, cur))
        if cur != last:
            prev = last
        self.prev[id(entity)] = (prev, cur)
        if entity.speed <= 0:
            return cur
        t = min(1.0, (monotonic() - entity.last_move) / entity.speed)
        return (prev[0] + (cur[0] - prev[0]) * t,
                prev[1] + (cur[1] - prev[1]) * t)

    def progress(self, entity):
        if entity.speed <= 0:
            return 1.0
        return min(1.0, (monotonic() - entity.last_move) / entity.speed)
