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


class Entity(ABC):
    def __init__(self, position, vitesse) -> None:
        self.start_pos = position
        self.current_pos = self.start_pos
        self.vitesse = vitesse
        self.direction = EntityDirection.DOWN
        self.next_direction: deque[tuple[int, int]] = deque()
        self.state = EntityState.NORMAL

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def reset(self):
        pass