from src import Pacman, EntityDirection


def test_entities():
    pacTest = Pacman((0, 0))
    assert pacTest.move(EntityDirection.UP) == pacTest.current_pos == -1, 0
