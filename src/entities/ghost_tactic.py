from .ghost import Ghost
from ..enums import EntityType, EntityDirection
from enum import Enum
from random import choice
from collections import deque


class PatrolState(Enum):
    PATROL = 1
    CHASE = 2


class GhostTactic(Ghost):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.entity_type = EntityType.GHOST
        self.patrol_state = PatrolState.PATROL
        self.patrol_target: tuple[int, int] | None = None
        self.coord_zone: list[tuple[int, int]] = []

    """
    this property find the different part of the matrix
    """

    @property
    def zone(self):
        matrix_y = len(self.engine.grid) - 1
        matrix_x = len(self.engine.grid[0]) - 1
        matrix_mid_y = len(self.engine.grid) // 2
        matrix_mid_x = len(self.engine.grid[0]) // 2
        sy, sx = self.start_pos

        if 0 <= sy < matrix_mid_y:
            if matrix_mid_x <= sx <= matrix_x:
                return (0, matrix_mid_y - 1, matrix_mid_x, matrix_x)
            return (0, matrix_mid_y - 1, 0, matrix_mid_x - 1)

        elif matrix_mid_y <= sy <= matrix_y:
            if matrix_mid_x <= sx <= matrix_x:
                return (matrix_mid_y, matrix_y, matrix_mid_x, matrix_x)
            return (matrix_mid_y, matrix_y, 0, matrix_mid_x - 1)

    def define_zone(self) -> None:
        self.coord_zone.clear()
        min_y, max_y, min_x, max_x = self.zone
        tmp = min_x

        while min_y <= max_y:
            while tmp <= max_x:
                self.coord_zone.append((min_y, tmp))
                tmp += 1
            tmp = min_x
            min_y += 1

    def normal_move(self):
        if self.patrol_target is None:
            self.patrol_target = choice(self.coord_zone)

        if self.patrol_state == PatrolState.PATROL:
            if self.current_pos == self.patrol_target:
                self.queue.clear()
                self.patrol_target = choice(self.coord_zone)
                self.algo_bfs(self.patrol_target)
            elif len(self.queue) == 0:
                self.algo_bfs(self.patrol_target)

        elif self.patrol_state == PatrolState.CHASE:
            if len(self.queue) == 0:
                self.algo_bfs(self.target)

    def algo_bfs(self, target: tuple[int, int]):
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
                        if new_neigh == target:
                            self.reverse_path(build_path, target)
                            return
                waiting_list.popleft()
            else:
                return

    def reverse_path(
            self, path: dict[tuple[int, int], tuple[int, int]],
            target: tuple[int, int]
            ) -> None:
        next_case: tuple[int, int] = target
        while next_case != self.current_pos:
            cy, cx = next_case
            py, px = path[next_case]
            dir = (cy - py, cx - px)
            self.queue.appendleft(EntityDirection(dir))
            next_case = path[next_case]

    def verifying_mode(self) -> None:
        ###
        # verify if pacman enter the patrol zone
        # verify the distance of the ghost with the zone
        # change patrol state and clear the queue
        ###
        ty, tx = self.target
        min_y, max_y, min_x, max_x = self.zone

        total = self.manhattan_dist(max_y, min_y, max_x, min_x)

        if (min_y <= ty <= max_y and min_x <= tx <= max_x
           and self.patrol_state == PatrolState.PATROL):

            if total == 0:
                self.reset_path()
                self.patrol_state = PatrolState.CHASE
            return

        if (total > 4 and self.patrol_state == PatrolState.CHASE):
            self.reset_path()
            self.patrol_target = choice(self.coord_zone)
            self.patrol_state = PatrolState.PATROL

    def manhattan_dist(self, max_y, min_y, max_x, min_x) -> int:
        gy, gx = self.current_pos
        total = 0

        if (gy > max_y):
            total += gy - max_y
        elif (gy < min_y):
            total += min_y - gy

        if (gx > max_x):
            total += gx - max_x
        elif (gx < min_x):
            total += min_x - gx

        return total

    def reset_path(self):
        self.queue.clear()
        self.visited.clear()

    def reset(self):
        self.patrol_state = PatrolState.PATROL
        self.patrol_target = None
        return super().reset()
