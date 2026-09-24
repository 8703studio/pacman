import pytest
from mazegenerator import MazeGenerator
from src import Engine

@pytest.fixture
def engine():
    mazegen = MazeGenerator((5,5))
    mazegen.generate()
    engine = Engine(mazegen.maze)
    return engine

def test_is_in_grid(engine):
    assert engine.is_in_grid((6,1)) == False
    assert engine.is_in_grid((5,5)) == False
    assert engine.is_in_grid((-1,3)) == False
    assert engine.is_in_grid((2,2)) == True
