from src.game.game import Game
from src.enums import GridObject, StateGame
from src.interface.audio_manager import AudioManager


class GameController:
    """Manage game updates and entity movements."""

    def __init__(
        self,
        logic: Game,
        audio_manager: AudioManager,
    ) -> None:
        """Initialize the game controller."""
        self.logic = logic
        self.audio_manager = audio_manager
        self.game_over_sound_played = False

    def consume_object_sound(self):
        if self.logic.last_object == GridObject.GUM:
            self.audio_manager.play_sound("pickup")

        if self.logic.last_object == GridObject.SUPERGUM:
            self.audio_manager.play_sound("powerup")

    def played_sound(
        self,
        lives_before: int,
        state_before: StateGame,
    ) -> None:
        if self.logic.life < lives_before:
            self.audio_manager.play_sound("hit")

        if (
            self.logic.gamestate == StateGame.GAMEOVER
            and not self.game_over_sound_played
        ):
            self.audio_manager.play_sound("GameOver")
            self.game_over_sound_played = True

        if (
            self.logic.gamestate == StateGame.VICTORY
            and state_before != StateGame.VICTORY
        ):
            self.audio_manager.play_sound("Victory")

    def update(self) -> None:
        """Update the game entities."""
        lives_before = self.logic.life
        state_before = self.logic.gamestate

        self.logic.update()
        self.played_sound(lives_before, state_before)
        self.consume_object_sound()
