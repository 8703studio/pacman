from enum import Enum


class StateGame(Enum):
    NEW = 0
    PAUSE = 1
    RESUME = 2
    GAMEOVER = 3
    VICTORY = 4


class GamePoint(Enum):
    GUM = 1
    SUPERGUM = 2
    GHOST = 3
    FRUIT = 4
