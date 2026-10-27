from collections import deque
from .entity import Entity
from ..enums import EntityType, EntityDirection


class Pacman(Entity):
    def __init__(self):
        super().__init__()
        self.entity_type = EntityType.PACMAN
        self.speed = 0.1
        self.input_buffer: deque[EntityDirection] = deque()

    def move(self):
        if self.queue:
            return
        if self.input_buffer:
            self.queue.append(self.input_buffer.popleft())

    def add_move_to_buffer(self, direction: EntityDirection):
        self.input_buffer.append(direction)

    def reset(self) -> None:
        self.input_buffer.clear()
        self.current_pos = self.start_pos
        self.queue.clear()
