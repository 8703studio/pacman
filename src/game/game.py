from time import monotonic

from ..config import GameConfig
from ..engine import Engine
from .level_handler import LevelHandler
from ..entities import GhostHandler, Pacman
from ..enums import (
    EntityState,
    EntityDirection,
    GamePoint,
    GridObject,
    StateGame,
)


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
        self.start_launch: float | None = monotonic()

        # Cheats
        self.freeze: bool = False
        self.spawn_f: float = monotonic()

    def update_speeds(self) -> None:
        """Adjust ghost speeds according to their state."""
        for ghost in self.ghosts.ghost_list:
            if ghost.state == EntityState.WEAK:
                ghost.speed = 0.4
            else:
                ghost.speed = 0.3

    def _object_point(self) -> dict[GamePoint, int]:
        dict_point: dict[GamePoint, int] = {}
        config_game = self.config.game_data()

        for obj, point in zip(GamePoint, config_game):
            dict_point[obj] = config_game[point]

        return dict_point

    @property
    def spawn_pacman(self) -> tuple[int, int]:
        spawn = self.levels.current_level
        return (
            len(spawn.grid) // 2,
            len(spawn.grid[0]) // 2,
        )

    def main_game(self) -> None:
        while self.run:
            pass

    def add_score(self, score: int) -> None:
        self.score += score

    def lose_life(self) -> None:
        """Remove one life and end the game if no lives remain."""
        if self.life <= 0:
            return

        self.life -= 1

        if self.life <= 0:
            self.life = 0
            self.run = False
            self.gamestate = StateGame.GAMEOVER

    def set_life(self) -> int:
        return self.config.lives

    def cheat_life(self) -> None:
        """Give Pac-Man 99 lives."""
        self.life = 99

    def cheat_freeze(self) -> None:
        """Toggle ghost movement on and off."""
        self.freeze = not self.freeze

    def cheat_invincibility(self) -> None:
        """Toggle Pac-Man invincibility."""
        if self.pacman.state == EntityState.NORMAL:
            self.pacman.state = EntityState.INVINCIBLE
        else:
            self.pacman.state = EntityState.NORMAL

    def spawn_fruit(self) -> None:
        """Fruit spawning is not implemented yet."""
        pass

    def change_level(self) -> bool:
        """Load the next level, or finish the game if none remains."""
        next_level = self.levels.next_level()

        if next_level is None:
            self.run = False
            self.gamestate = StateGame.VICTORY
            return True

        self.engine.grid = next_level.grid

        self.pacman.start_pos = (
            len(next_level.grid) // 2,
            len(next_level.grid[0]) // 2,
        )
        self.pacman.reset()
        self.pacman.state = EntityState.NORMAL

        self.freeze = False
        self.ghosts.set_spawn_ghost(next_level.corners)

        for ghost in self.ghosts.ghost_list:
            ghost.state = EntityState.NORMAL
            ghost.reset()

        self.weak_start = None

        next_level.start()
        self.start_launch = monotonic()
        self.gamestate = StateGame.NEW

        return False

    def pause_game(self) -> None:
        if self.gamestate != StateGame.RESUME:
            return

        self.start_pause = monotonic()
        self.gamestate = StateGame.PAUSE

    def resume_game(self) -> None:
        if self.gamestate != StateGame.PAUSE:
            return

        if self.start_pause is None:
            return

        duration_pause = monotonic() - self.start_pause

        if self.weak_start is not None:
            self.weak_start += duration_pause

        level = self.levels.current_level

        if level.start_timer is not None:
            level.start_timer += duration_pause

        for ghost in self.ghosts.ghost_list:
            if ghost.last_move is not None:
                ghost.last_move += duration_pause

        if self.pacman.last_move is not None:
            self.pacman.last_move += duration_pause

        self.start_pause = None
        self.gamestate = StateGame.RESUME

    def set_ghost_state(self) -> None:
        """Make all living ghosts weak."""
        self.weak_start = monotonic()

        for ghost in self.ghosts.ghost_list:
            if ghost.state != EntityState.DEAD:
                ghost.reset()
                ghost.set_state(EntityState.WEAK)

    def verify_dead_ghost(self) -> None:
        """Restore ghosts when they return to their spawn position."""
        for ghost in self.ghosts.ghost_list:
            if (
                ghost.state == EntityState.DEAD
                and ghost.current_pos == ghost.start_pos
            ):
                ghost.reset()

                if self.weak_start is not None:
                    ghost.set_state(EntityState.WEAK)
                else:
                    ghost.set_state(EntityState.NORMAL)

    def update_weak_time(self) -> None:
        """End the temporary weak state after the timer expires."""
        if self.weak_start is None:
            return

        elapsed = monotonic() - self.weak_start

        if elapsed >= self.weak_time:
            for ghost in self.ghosts.ghost_list:
                if ghost.state == EntityState.WEAK:
                    ghost.reset()
                    ghost.set_state(EntityState.NORMAL)

            self.weak_start = None

    def pacman_movement(
        self,
        input_direction: EntityDirection,
    ) -> None:
        """Buffer the requested direction and move Pac-Man."""
        self.pacman.add_move_to_buffer(input_direction)

        if not self.pacman.can_move():
            return

        self.pacman.move()
        move = self.pacman.next_move()

        if move is None:
            return

        if not self.engine.is_valid_position(
            move.value,
            self.pacman.current_pos,
        ):
            return

        self.pacman.update_entity(move.value)

        obj = self.levels.current_level.consume_object(self.pacman.current_pos)

        if obj == GridObject.SUPERGUM:
            self.set_ghost_state()

        if obj != GridObject.EMPTY:
            self.add_score(self.point[GamePoint[obj.name]])

    def ghosts_movement(self) -> None:
        """Move ghosts towards Pac-Man."""
        for ghost in self.ghosts.ghost_list:
            if not ghost.can_move():
                continue

            ghost.target = self.pacman.current_pos
            ghost.move()
            move_ghost = ghost.next_move()

            if move_ghost is None:
                continue

            if self.engine.is_valid_position(
                move_ghost.value,
                ghost.current_pos,
            ):
                ghost.update_entity(move_ghost.value)

    def check_collision(self) -> bool:
        """Handle collisions between Pac-Man and ghosts."""
        for ghost in self.ghosts.ghost_list:
            if ghost.state == EntityState.DEAD:
                continue

            if ghost.current_pos != self.pacman.current_pos:
                continue

            if ghost.state == EntityState.WEAK:
                ghost.state = EntityState.DEAD
                self.add_score(self.point[GamePoint.GHOST])
                continue

            if self.pacman.state == EntityState.INVINCIBLE:
                continue

            self.lose_life()
            self.pacman.reset()
            self.weak_start = None

            for other in self.ghosts.ghost_list:
                other.current_pos = other.start_pos
                other.state = EntityState.NORMAL
                other.reset()

            return True

        return False

    def update(
        self,
        input_direction: EntityDirection,
    ) -> None:
        """Update the game state and all entities."""
        level = self.levels.current_level

        if self.start_launch is None:
            return

        if self.gamestate == StateGame.NEW:
            elapsed = monotonic() - self.start_launch

            if elapsed <= 3:
                return

            self.gamestate = StateGame.RESUME
            level.start_timer = monotonic()

        if self.gamestate in (
            StateGame.PAUSE,
            StateGame.VICTORY,
            StateGame.GAMEOVER,
        ):
            return

        if level.remaining_time() <= 0:
            self.run = False
            self.gamestate = StateGame.GAMEOVER
            return

        self.update_weak_time()
        self.pacman_movement(input_direction)

        if self.check_collision():
            return

        if self.levels.current_level.is_finished():
            self.change_level()
            return

        if not self.freeze:
            self.ghosts_movement()

        self.verify_dead_ghost()
        self.check_collision()
