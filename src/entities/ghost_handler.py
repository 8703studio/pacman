from .entity import Entity


class GhostHandler():
    def __init__(self, ghost_list: list[Entity]):
        self.ghost_list = ghost_list

    def set_spawn_ghost(self, corner_level: list[tuple[int, int]]):
        for ghost, pos in zip(self.ghost_list, corner_level):
            ghost.start_pos = pos
            ghost.current_pos = pos

    def move_ghost_list(self):
        pass
