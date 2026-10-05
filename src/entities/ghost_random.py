from entity import Entity, EntityType
from ghost import Ghost


class GhostRandom(Entity, Ghost):
    def __init__(self, position):
        super().__init__(position)
        self.entity_type = EntityType.GHOST

    def move(self):
        return super().move()

    def reset(self):
        return super().reset()
