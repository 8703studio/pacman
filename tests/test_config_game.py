from src.config.game_config import GameConfig


def test_level_data():
    config = GameConfig()

    data = config.level_data()

    assert data["levels"] == config.levels
    assert data["seed"] == config.seed


def test_game_data():
    config = GameConfig()

    data = config.game_data()

    assert data["pointperpacgum"] == config.pointperpacgum
    assert data["pointpersuperpacgum"] == config.pointpersuperpacgum
    assert data["pointperghost"] == config.pointperghost
    assert data["lives"] == config.lives
    assert data["levelsmaxtime"] == config.levelsmaxtime
