# matrice contenant les objets creer a partir du maze
from ..config import GameConfig
from ..engine import Engine
from .level_handler import LevelHandler
from ..entities import GhostHandler, Pacman
from ..enums import EntityState, GamePoint, GridObject
from time import monotonic
# , ghost_handler, engine, level_handler, pacman, config)


class Game():
    def __init__(self, ghost_handler: GhostHandler, engine: Engine,
                 level_handler: LevelHandler,
                 pacman: Pacman, config: GameConfig) -> None:

        self.config: GameConfig = config
        self.ghosts: GhostHandler = ghost_handler
        self.engine: Engine = engine
        self.levels: LevelHandler = level_handler
        self.pacman: Pacman = pacman
        self.score: int = 0
        self.life: int = self.set_life()
        self.point: dict[GamePoint, int] = self._object_point()
        self.run: bool = True
        self.weak_time: int = 8
        self.weak_start: float | None = None

    def _object_point(self):
        dict_point: dict[GamePoint, int] = {}
        config_game = self.config.game_data()

        for obj, point in zip(GamePoint, config_game):
            dict_point[obj] = config_game[point]

        return dict_point

    @property
    def spawn_pacman(self):
        spawn = self.levels.current_level
        return (len(spawn.grid) // 2, len(spawn.grid[0]) // 2)

    def main_game(self):
        while self.run:
            pass

    def add_score(self, score: int):
        self.score += score

    def lose_life(self):
        self.life -= 1

    def set_life(self) -> int:
        return self.config.lives

    def change_level(self):
        pass

    def set_ghost_state(self):
        self.weak_start = monotonic()

        for ghost in self.ghosts.ghost_list:
            if ghost.state != EntityState.DEAD:
                ghost.set_state(EntityState.WEAK)

    def update_weak_time(self):
        if self.weak_start is None:
            return

        elapsed = monotonic() - self.weak_start

        if elapsed >= self.weak_time:
            for ghost in self.ghosts.ghost_list:
                if ghost.state == EntityState.WEAK:
                    ghost.set_state(EntityState.NORMAL)
                    self.weak_start = None

    def pacman_movement(self):
        if not self.pacman.can_move():
            return

        self.pacman.move()
        move = self.pacman.next_move()

        if move is not None:
            if self.engine.is_valid_position(move.value,
                                             self.pacman.current_pos):
                self.pacman.update_entity(move.value)
                obj = self.levels.current_level.consume_object(self
                                                               .pacman.
                                                               current_pos)
                if obj == GridObject.SUPERGUM:
                    self.set_ghost_state()

                if obj != GridObject.EMPTY:
                    self.add_score(self.point[GamePoint[obj.name]])

    def ghosts_movement(self):
        for ghost in self.ghosts.ghost_list:
            if not ghost.can_move():
                continue

            ghost.move()
            move_ghost = ghost.next_move()

            if move_ghost is not None:
                if self.engine.is_valid_position(move_ghost.value,
                                                 ghost.current_pos):
                    ghost.update_entity(move_ghost.value)

    def check_collision(self):
        for ghost in self.ghosts.ghost_list:
            if ghost.current_pos == self.pacman.current_pos:
                if ghost.state == EntityState.WEAK:
                    ghost.state = EntityState.DEAD
                    self.add_score(self.point[GamePoint.GHOST])
                    return False
                else:
                    if ghost.state is not EntityState.DEAD:
                        self.lose_life()
                        self.pacman.reset()
                        return True

    def update(self):
        level = self.levels.current_level

        if level.remaining_time() <= 0:
            self.run = False
            return
        self.update_weak_time()

        self.pacman_movement()

        if self.check_collision():
            return

        if self.levels.current_level.is_finished():
            self.change_level()
            return
        
        self.ghosts_movement()
        self.check_collision()
