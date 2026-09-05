from abc import ABC, abstractmethod
from enum import Enum
from collections import deque

# tuple (line, column)


class EntityDirection(Enum):
    UP = (-1, 0)
    LEFT = (0, -1)
    DOWN = (1, 0)
    RIGHT = (0, 1)


class EntityState(Enum):
    NORMAL = 1
    WEAK = 2
    DEAD = 3


class EntityType(Enum):
    NULL = 0
    PACMAN = 1
    GHOST = 2


class Entity(ABC):
    def __init__(self, position, vitesse) -> None:
        self.start_pos = position
        self.current_pos = self.start_pos
        self.vitesse = vitesse
        self.direction = EntityDirection.DOWN
        self.next_direction: deque[tuple[int, int]] = deque()
        self.state = EntityState.NORMAL
        self.entity_type = EntityType.NULL

    @abstractmethod
    def move(self) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


class Pacman(Entity):
    def __init__(self, position, vitesse):
        super().__init__(position, vitesse)
        self.entity_type = EntityType.PACMAN

    def move(self) -> None:
        pass

    def reset(self) -> None:
        self.current_pos = self.start_pos

    def eat(self) -> None:
        pass
