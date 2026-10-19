from ..enums import EntityType, EntityDirection
from ..engine import Engine
from .ghost import Ghost
from math import dist
import random


class GhostGlutton(Ghost):
    def __init__(self, engine: Engine):
        super().__init__()
        self.entity_type = EntityType.GHOST
        self.engine = engine
        self.opposite_dir = {
            EntityDirection.RIGHT: EntityDirection.LEFT,
            EntityDirection.LEFT: EntityDirection.RIGHT,
            EntityDirection.UP: EntityDirection.DOWN,
            EntityDirection.DOWN: EntityDirection.UP
        }

    def normal_move(self):
        euclidean_dict = {}
        list_direction = self.engine.get_valid_position(self.current_pos)

        if self.last_dir is not None:
            if self.opposite_dir[self.last_dir] in list_direction:
                list_direction.remove(self.opposite_dir[self.last_dir])
                if len(list_direction) == 0:
                    self.queue.append(self.opposite_dir[self.last_dir])
                    return

        for direction in list_direction:
            dy, dx = direction.value
            cy, cx = self.current_pos
            next_case = (cy + dy, dx + cx)
            euclidean_dict[direction] = dist(next_case, self.target)

        min_val = min(euclidean_dict.values())
        res = [k for k, v in euclidean_dict.items() if v == min_val]
        self.queue.append(random.choice(res))
        return

    def reset(self):
        return super().reset()
