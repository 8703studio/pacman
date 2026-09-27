from abc import ABC, abstractmethod
from ..enums import EntityType, EntityState, EntityDirection

# tuple (line, column)


class Entity(ABC):
    def __init__(self, position) -> None:
        self.start_pos = position
        self.current_pos = self.start_pos
        self.vitesse = 0
        self.direction = EntityDirection.DOWN
        self.state = EntityState.NORMAL
        self.entity_type = EntityType.NULL

    @abstractmethod
    def move(self, direction) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass



