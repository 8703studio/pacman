from .entity import Entity
from ..enums import EntityType


class GhostChaser(Entity):
    def __init__(self):
        super().__init__()
        self.entity_type = EntityType.GHOST

    def move(self):
        explo_queue = []
        '''
            faire le code du bfs 
        '''
        return explo_queue[0]

    def reset(self):
        return super().reset()
