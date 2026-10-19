from src.engine.physics import Engine
from src.game.game import Game

# from src.entities.ghost import Ghost
from src.entities.ghost_interceptor import GhostInterceptor
from src.enums import GamePoint, GridObject
from src.interface.audio_manager import AudioManager


class GameController:
    """Manage game updates and entity movements."""

    def __init__(
        self,
        logic: Game,
        ghost: GhostInterceptor,
        audio_manager: AudioManager,
    ) -> None:
        """Initialize the game controller."""

        self.logic = logic
        self.ghost = ghost
        self.audio_manager = audio_manager

    def update(self, maze) -> None:
        """Update the game entities."""

        if maze is None or not self.logic.run:
            return

        self.logic.update_weak_time()
        pacman = self.logic.pacman
        pacman.move()
        direction = pacman.next_move()

        if direction is not None:
            vector = direction.value
            engine = Engine(maze)

            if engine.is_valid_position(
                vector,
                pacman.current_pos,
            ):
                pacman.direction = direction
                pacman.update_entity(vector)

            obj = self.logic.levels.current_level.consume_object(
                pacman.current_pos
            )

            if obj != GridObject.EMPTY:
                self.logic.add_score(self.logic.point[GamePoint[obj.name]])

            if obj == GridObject.GUM:
                self.audio_manager.play_sound("pickup")

            if obj == GridObject.SUPERGUM:
                self.logic.set_ghost_state()
                self.audio_manager.play_sound("powerup")

        lives_before = self.logic.life

        if self.logic.check_collision():
            if self.logic.life < lives_before:
                self.audio_manager.play_sound("hit")

                if not self.logic.run:
                    self.audio_manager.play_sound("GameOver")
            return

        engine = Engine(maze)

        for ghost in self.logic.ghosts.ghost_list:
            if isinstance(ghost, GhostInterceptor):
                ghost.engine = engine
                ghost.pacman_position = pacman.current_pos
                ghost.pacman_direction = pacman.direction
            else:
                ghost.target = pacman.current_pos

            if isinstance(ghost, GhostInterceptor):
                ghost.move()
            else:
                if not ghost.can_move():
                    continue
                ghost.move()

            ghost.move()
            direction = ghost.next_move()

            if direction is None:
                continue

            vector = direction.value

            if engine.is_valid_position(vector, ghost.current_pos):
                ghost.direction = direction
                ghost.update_entity(vector)

        lives_before = self.logic.life

        if self.logic.check_collision():
            if self.logic.life < lives_before:
                self.audio_manager.play_sound("hit")

                if not self.logic.run:
                    self.audio_manager.play_sound("GameOver")

        if self.logic.run and self.logic.levels.current_level.is_finished():
            if self.logic.change_level():
                self.audio_manager.play_sound("Victory")
