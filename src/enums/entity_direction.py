from enum import Enum


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
