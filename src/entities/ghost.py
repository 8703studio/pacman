from .entity import Entity
from abc import ABC, abstractmethod
from ..enums import EntityState


class Ghost(Entity, ABC):
    def __init__(self) -> None:
        super().__init__()

    def move(self) -> None:
        if self.state == EntityState.NORMAL:
            self.normal_move()

        if self.state == EntityState.WEAK:
            pass

        if self.state == EntityState.DEAD:
            pass

    @abstractmethod
    def normal_move(self):
        pass

    def weak_move(self):
        pass

    def dead_move(self):
        pass
