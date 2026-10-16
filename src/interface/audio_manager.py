from pathlib import Path

import pygame


class AudioManager:
    """Load and control the game's sound effects."""

    def __init__(self) -> None:
        """Initialize sound settings and load available sound effects."""
        self.sound_enabled = True
        self.music_enabled = True

        sounds_dir = (
            Path(__file__).resolve().parent / "assets" / "sounds"
        )
        self.sounds: dict[str, pygame.mixer.Sound] = {}

        if pygame.mixer.get_init() is None:
            pygame.mixer.init()

        for path in sounds_dir.glob("*.wav"):
            self.sounds[path.stem] = pygame.mixer.Sound(str(path))

    def play_sound(self, name: str) -> None:
        """Play a sound effect if sound is enabled."""
        if not self.sound_enabled:
            return

        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()

    def set_sound_enabled(self, enabled: bool) -> None:
        """Enable or disable sound effects."""
        self.sound_enabled = enabled
