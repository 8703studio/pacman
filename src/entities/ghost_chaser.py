from entity import Entity, EntityType


class GhostChaser(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.entity_type = EntityType.GHOST

    def move(self):
        return super().move()

    def reset(self):
        return super().reset()
