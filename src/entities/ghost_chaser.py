from src.enums import EntityDirection
from collections import deque
from .ghost import Ghost
from ..enums import EntityType
from ..engine import Engine


class GhostChaser(Ghost):
    def __init__(self, engine: Engine):
        super().__init__()
        self.entity_type = EntityType.GHOST
        self.engine = engine

    def normal_move(self):
        if len(self.queue) == 0:
            build_path = {}
            waiting_list = deque()
            waiting_list.appendleft(self.current_pos)
            self.visited.add(self.current_pos)

            while waiting_list:
                if self.target in waiting_list:
                    break

                for case_neigh in self.neighboor:
                    ny, nx = case_neigh
                    cy, cx = waiting_list[0]
                    new_neigh = (cy + ny, cx + nx)
                    if new_neigh in self.visited:
                        continue

                    if self.engine.is_valid_position(case_neigh,
                                                     waiting_list[0]):
                        waiting_list.append(new_neigh)
                        build_path[new_neigh] = waiting_list[0]
                        self.visited.add(new_neigh)

                waiting_list.popleft()
        else:
            return

    def reset(self):
        return super().reset()
