from .ghost import Ghost
from ..enums import EntityType


class GhostChaser(Ghost):
    def __init__(self):
        super().__init__()
        self.entity_type = EntityType.GHOST

    def move(self):
        pass

    def reset(self):
        return super().reset()
