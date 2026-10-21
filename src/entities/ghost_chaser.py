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
            self.visited.clear()
            build_path = {}
            waiting_list = deque()
            waiting_list.appendleft(self.current_pos)
            self.visited.add(self.current_pos)

            while waiting_list:

                for case_neigh in self.neighboor:
                    ny, nx = case_neigh
                    cy, cx = waiting_list[0]
                    new_neigh = (cy + ny, cx + nx)
                    if new_neigh in self.visited:
                        continue

                    if self.engine.is_valid_position(
                        case_neigh, waiting_list[0]
                    ):
                        waiting_list.append(new_neigh)
                        build_path[new_neigh] = waiting_list[0]
                        self.visited.add(new_neigh)
                        if new_neigh == self.target:
                            self.reverse_path(build_path)
                            return

                waiting_list.popleft()
        else:
            return

    def reverse_path(
        self, path: dict[tuple[int, int], tuple[int, int]]
    ) -> None:
        next_case: tuple[int, int] = self.target
        while next_case != self.current_pos:
            cy, cx = next_case
            py, px = path[next_case]
            dir = (cy - py, cx - px)
            self.queue.appendleft(EntityDirection(dir))
            next_case = path[next_case]
            print(next_case)
        print(self.queue)

    def reset(self):
        return super().reset()
