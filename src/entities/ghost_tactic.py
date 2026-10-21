from .ghost import Ghost
from ..enums import EntityType
from enum import Enum
from random import choice


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

        elif self.patrol_state == PatrolState.CHASE:
            if len(self.queue) == 0:
                self.algo_bfs(self.target)

    def algo_bfs(self, target: tuple[int, int]):
        pass

    def verifying_mode(self):
        pass
    ### 
    # verify if pacman enter the patrol zone
    # verify the distance of the ghost with the zone
    # change patrol state and clear the queue  
    ###

    def reset(self):
        self.patrol_state = PatrolState.PATROL
        return super().reset()
