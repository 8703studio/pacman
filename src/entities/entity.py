from abc import ABC, abstractmethod
from ..enums import EntityType, EntityState, EntityDirection
from collections import deque


class Entity(ABC):
    def __init__(self) -> None:
        self.start_pos = (0, 0)
        self.current_pos = self.start_pos
        self.vitesse = 0
        self.direction = EntityDirection.DOWN
        self.state = EntityState.NORMAL
        self.entity_type = EntityType.NULL
        self.queue: deque[tuple[int, int]] = deque()
        self.visited: deque[tuple[int, int]] = deque()

    @abstractmethod
    def move(self) -> tuple[int, int]:
        pass

    def update_entity(self, direction: tuple[int, int]) -> None:
        cy, cx = self.current_pos
        dy, dx = direction
        self.current_pos = (cy + dy, cx + dx)

    @abstractmethod
    def reset(self) -> None:
        pass

    def set_state(self, state: EntityState):
        self.state = state

    def get_state(self) -> EntityState:
        return self.state
