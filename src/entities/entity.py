from abc import ABC, abstractmethod
from enum import Enum
from collections import deque

# tuple (line, column)
Position = tuple[int, int]


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
    def __init__(self, position: Position) -> None:
        self.start_pos: Position = position
        self.current_pos: Position = self.start_pos
        self.vitesse: float = 0
        self.direction: EntityDirection = EntityDirection.DOWN
        self.state: EntityState = EntityState.NORMAL
        self.entity_type: EntityType = EntityType.NULL

    @abstractmethod
    def move(self, direction: tuple[int, int]) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


class Pacman(Entity):
    def __init__(self, position: Position) -> None:
        super().__init__(position)
        self.entity_type = EntityType.PACMAN
        self.vitesse = 0.5
        self.input_buffer: deque[Position] = deque()

    def move(self, direction: tuple[int, int]) -> None:
        d_x, d_y = direction
        x_pos, y_pos = self.current_pos
        self.current_pos = (x_pos + d_x, y_pos + d_y)
        self.direction = EntityDirection(direction)

    def reset(self) -> None:
        self.input_buffer.clear()
        self.current_pos = self.start_pos
