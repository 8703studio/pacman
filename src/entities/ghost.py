from .entity import Entity
from abc import ABC, abstractmethod
from ..enums import EntityState
from time import monotonic


class Ghost(Entity, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.target: tuple[int, int] | None = None
        self.neighboor = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

    def move(self) -> None:
        if self.state == EntityState.NORMAL:
            self.normal_move()

        if self.state == EntityState.WEAK:
            self.weak_move()

        if self.state == EntityState.DEAD:
            self.dead_move()

    @abstractmethod
    def normal_move(self):
        pass

    def weak_move(self):
        pass

    def dead_move(self):
        pass

    def reset(self) -> None:
        super().reset()
        self.last_move = monotonic()
        self.last_dir = None

