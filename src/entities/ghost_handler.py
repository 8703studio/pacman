from .ghost import Ghost


class GhostHandler():
    def __init__(self, ghost_list: list[Ghost]):
        self.ghost_list = ghost_list

    def set_spawn_ghost(self, corner_level: list[tuple[int, int]]) -> None:
        for ghost, pos in zip(self.ghost_list, corner_level):
            ghost.start_pos = pos
            ghost.current_pos = pos

    def move_ghost_list(self):
        listes = []
        for ghost in self.ghost_list:
            listes.append(ghost)
        return listes
