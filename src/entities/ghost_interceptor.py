from .entity import Entity
from ..enums import EntityType


class GhostInterceptor(Entity):
    def __init__(self):
        super().__init__()
        self.entity_type = EntityType.GHOST

    def move(self):
        return super().move()

    def reset(self):
        return super().reset()
