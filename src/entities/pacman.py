from collections import deque
from .entity import Entity
from ..enums import EntityType


class Pacman(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.entity_type = EntityType.PACMAN
        self.vitesse = 0.5
        self.input_buffer: deque[tuple[int, int]] = deque()

    def next_direction(self):
        if len(self.input_buffer) != 0:
            return self.input_buffer[0]

    def move_intent(self, direction):
        ny, nx = self.input_buffer[0]

    def advance(self) -> None:
        d_y, d_x = self.direction.value
        y_pos, x_pos = self.current_pos
        self.current_pos = (y_pos + d_y, x_pos + d_x)

    def reset(self) -> None:
        self.input_buffer.clear()
        self.current_pos = self.start_pos
