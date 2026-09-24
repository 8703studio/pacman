from mazegenerator import MazeGenerator
import pytest

@pytest.fixture
def mazegen():
    mazegen = MazeGenerator((5,5))
    mazegen.generate()
    return mazegen

def test_maze(mazegen):
    assert len(mazegen.maze) == 5

def test_len_maze(mazegen):
    for i in mazegen.maze:
            assert len(i) == 5

def test_case_value(mazegen):
    for row in mazegen.maze:
        for cell in row:
            assert isinstance(cell, int)

def test_wall_north_line_0(mazegen):
    for cell in mazegen.maze[0]:
        assert cell & 1 != 0

def test_case_west_wall_colum_0(mazegen):
    test = [row[0] for row in mazegen.maze]
    print(test)
    for value in test:
        assert value & 8 !=0

def test_case_east_wall_last_column(mazegen):
    test = [row[-1] for row in mazegen.maze]
    print(test)
    for value in test:
        assert value & 2 !=0


def test_case_south_wall_last_line(mazegen):
    for value in mazegen.maze[-1]:
        assert value & 4 !=0