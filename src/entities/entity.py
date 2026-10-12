from abc import ABC, abstractmethod
from ..enums import EntityType, EntityState, EntityDirection
from collections import deque


class Entity(ABC):
    def __init__(self) -> None:
        self.start_pos: tuple[int, int] = (0, 0)
        self.current_pos: tuple[int, int] = self.start_pos
        self.vitesse = 0
        self.direction = EntityDirection.DOWN
        self.state = EntityState.NORMAL
        self.entity_type = EntityType.NULL
        self.queue: deque[EntityDirection] = deque()
        self.visited: set[tuple[int, int]] = set()

    @abstractmethod
    def move(self) -> None:
        pass

    def next_move(self) -> EntityDirection | None:
        if len(self.queue) != 0:
            return self.queue.popleft()
        return None

    def update_entity(self, direction: tuple[int, int]) -> None:
        cy, cx = self.current_pos
        dy, dx = direction
        self.current_pos = (cy + dy, cx + dx)

    def reset(self) -> None:
        self.queue.clear()
        self.visited.clear()

    def set_state(self, state: EntityState):
        self.state = state

    def get_state(self) -> EntityState:
        return self.state
