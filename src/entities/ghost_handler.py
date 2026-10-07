from ghost import Ghost


class GhostHandler():
    def __init__(self, ghost_list: list[Ghost]):
        self.ghost_list = ghost_list

    def move_ghost_list(self):
        for ghost in self.ghost_list:
            direction = ghost.queue[0]
