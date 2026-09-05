from entity import Entity, EntityType, EntityState, EntityDirection


class Hoshi_ghost_1(Entity):
    def __init__(self, position, vitesse):
        super().__init__(position, vitesse)
        self.entity_type = EntityType.GHOST

    def move(self):
        return super().move()

    def reset(self):
        return super().reset()


class Joy_ghost_2(Entity):
    def __init__(self, position, vitesse):
        super().__init__(position, vitesse)
        self.entity_type = EntityType.GHOST

    def move(self):
        return super().move()

    def reset(self):
        return super().reset()


class Momo_ghost_3(Entity):
    def __init__(self, position, vitesse):
        super().__init__(position, vitesse)
        self.entity_type = EntityType.GHOST

    def move(self):
        return super().move()

    def reset(self):
        return super().reset()
