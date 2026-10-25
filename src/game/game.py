# matrice contenant les objets creer a partir du maze
from ..config import GameConfig
from ..engine import Engine
from .level_handler import LevelHandler
from ..entities import GhostHandler, Pacman, GhostTactic
from ..enums import (
    EntityState,
    GamePoint,
    GridObject,
    StateGame,
    EntityDirection,
)
from time import monotonic

# , ghost_handler, engine, level_handler, pacman, config)


class Game:
    def __init__(
        self,
        ghost_handler: GhostHandler,
        engine: Engine,
        level_handler: LevelHandler,
        pacman: Pacman,
        config: GameConfig,
    ) -> None:

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

        self.gamestate: StateGame = StateGame.NEW
        self.start_pause: float | None = None
        self.start_launch = monotonic()

        self.freeze: bool = False
        self.spawn_f = monotonic()
        self.last_object = GridObject.EMPTY

    def update_speeds(self) -> None:
        """Adjust ghost speeds according to their state."""
        for ghost in self.ghosts.ghost_list:
            if ghost.state == EntityState.WEAK:
                ghost.speed = 0.4
            else:
                ghost.speed = 0.3

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

    def add_score(self, score: int):
        self.score += score

    def lose_life(self) -> None:
        self.life -= 1

        if self.life <= 0:
            self.life = 0
            self.gamestate = StateGame.GAMEOVER
            self.run = False
            return

    def set_life(self) -> int:
        return self.config.lives

    def cheat_life(self) -> None:
        self.life = 99

    def cheat_freeze(self) -> None:
        self.freeze = not self.freeze
        print("CHEAT :", self.freeze, id(self))

    def cheat_invincibility(self) -> None:
        if self.pacman.state == EntityState.NORMAL:
            self.pacman.state = EntityState.INVINCIBLE
            return
        self.pacman.state = EntityState.NORMAL

    def spawn_fruit(self):
        pass

    def change_level(self) -> None | bool:
        nlevel = self.levels.next_level()
        if nlevel is None:
            return
        self.engine.grid = nlevel.grid
        self.pacman.start_pos = (
            len(nlevel.grid) // 2,
            len(nlevel.grid[0]) // 2,
        )
        self.pacman.reset()
        self.freeze = False
        self.pacman.state = EntityState.NORMAL
        self.ghosts.set_spawn_ghost(nlevel.corners)

        for ghost in self.ghosts.ghost_list:
            ghost.state = EntityState.NORMAL
            ghost.reset()
        self.weak_start = None
        return True

    def pause_game(self) -> None:
        if self.gamestate != StateGame.RESUME:
            return
        self.start_pause = monotonic()
        self.gamestate = StateGame.PAUSE

    def resume_game(self) -> None:
        if self.gamestate != StateGame.PAUSE:
            return

        if self.start_pause is not None:
            duration_pause = monotonic() - self.start_pause

            if self.weak_start is not None:
                self.weak_start += duration_pause

            if self.levels.current_level.start_timer is not None:
                self.levels.current_level.start_timer += duration_pause

            for ghost in self.ghosts.ghost_list:
                if ghost.last_move is not None:
                    ghost.last_move += duration_pause

            if self.pacman.last_move is not None:
                self.pacman.last_move += duration_pause

            self.start_pause = None
            self.gamestate = StateGame.RESUME

    def set_ghost_state(self) -> None:
        self.weak_start = monotonic()

        for ghost in self.ghosts.ghost_list:
            if ghost.state != EntityState.DEAD:
                ghost.reset()
                ghost.set_state(EntityState.WEAK)

    def verify_dead_ghost(self) -> None:
        for ghost in self.ghosts.ghost_list:
            if ghost.state == EntityState.DEAD:
                if ghost.current_pos == self.pacman.current_pos:
                    continue

                if ghost.current_pos == ghost.start_pos:

                    if self.weak_start is not None:
                        continue
                    ghost.reset()
                    ghost.state = EntityState.NORMAL

    def update_weak_time(self) -> None:
        if self.weak_start is None:
            return

        elapsed = monotonic() - self.weak_start

        if elapsed >= self.weak_time:
            for ghost in self.ghosts.ghost_list:
                if ghost.state == EntityState.WEAK:
                    ghost.reset()
                    ghost.set_state(EntityState.NORMAL)
            self.weak_start = None

    def pacman_movement(self) -> None:
        if not self.pacman.can_move():
            return

        self.pacman.move()
        move = self.pacman.next_move()

        if move is not None:
            if self.engine.is_valid_position(
                move.value, self.pacman.current_pos
            ):
                self.pacman.update_entity(move.value)
                obj = self.levels.current_level.consume_object(
                    self.pacman.current_pos
                )
                self.last_object = obj
                if obj == GridObject.SUPERGUM:
                    self.set_ghost_state()

                if obj != GridObject.EMPTY:
                    self.add_score(self.point[GamePoint[obj.name]])

    def ghosts_movement(self) -> None:
        if self.freeze:
            return

        for ghost in self.ghosts.ghost_list:
            if not ghost.can_move():
                continue

            ghost.target = self.pacman.current_pos
            if (ghost.state == EntityState.NORMAL or
                ghost.state == EntityState.WEAK or
               ghost.state == EntityState.DEAD):

                ghost.move()
                move_ghost = ghost.next_move()

                if move_ghost is not None:
                    if self.engine.is_valid_position(
                        move_ghost.value, ghost.current_pos
                    ):
                        ghost.update_entity(move_ghost.value)
            else:
                continue

    def check_collision(self) -> bool:
        if self.pacman.state == EntityState.INVINCIBLE:
            return False

        for ghost in self.ghosts.ghost_list:
            if ghost.state == EntityState.DEAD:
                continue

            if ghost.current_pos != self.pacman.current_pos:
                continue

            if ghost.state == EntityState.WEAK:
                print("FANTÔME MANGÉ :", ghost.current_pos, ghost.start_pos)
                ghost.state = EntityState.DEAD
                self.add_score(self.point[GamePoint.GHOST])
                continue

            self.lose_life()
            self.pacman.reset()
            self.weak_start = None

            for other in self.ghosts.ghost_list:
                other.state = EntityState.NORMAL
                other.reset()
                other.current_pos = other.start_pos

            return True

        return False

    def update(self) -> None:
        level = self.levels.current_level
        self.last_object = GridObject.EMPTY

        if self.start_launch is None:
            return

        if self.gamestate == StateGame.NEW:
            elapsed = monotonic() - self.start_launch
            if elapsed <= 3:
                return
            self.gamestate = StateGame.RESUME
            level.start_timer = monotonic()

        if (
            self.gamestate == StateGame.PAUSE
            or self.gamestate == StateGame.VICTORY
            or self.gamestate == StateGame.GAMEOVER
        ):
            return

        self.update_weak_time()

        if (self.levels.current_level.remaining_time() <= 0
           and not self.levels.current_level.is_finished()):

            self.gamestate = StateGame.GAMEOVER
            self.run = False
            return

        self.pacman_movement()

        if self.check_collision():
            return

        if self.levels.current_level.is_finished():
            if self.change_level() is not None:
                self.start_launch = monotonic()
                self.gamestate = StateGame.NEW
            else:
                self.gamestate = StateGame.VICTORY
                self.run = False
            return

        self.ghosts_movement()
        self.verify_dead_ghost()
        self.check_collision()
