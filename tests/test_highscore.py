
import json

import pytest

from src.game.highscore import Highscore


def test_add_valid_score(tmp_path):
    """Test adding and saving a valid score."""
    path = tmp_path / "highscore.json"
    highscore = Highscore(str(path))

    result = highscore.add_score("EMILIE", 100)

    assert result is True
    assert highscore.scores == [
        {"name": "EMILIE", "score": 100}
    ]

    data = json.loads(path.read_text())
    assert data == highscore.scores


@pytest.mark.parametrize(
    ("name", "score"),
    [
        ("", 100),
        ("ABCDEFGHIJK", 100),
        ("EMILIE!", 100),
        ("EMILIE", -1),
        ("EMILIE", True),
        (123, 100),
    ],
)
def test_add_invalid_score(tmp_path, name, score):
    """Test rejecting invalid names and scores."""
    path = tmp_path / "highscore.json"
    highscore = Highscore(str(path))

    result = highscore.add_score(name, score)

    assert result is False
    assert highscore.scores == []
    assert not path.exists()


def test_scores_are_sorted_and_limited(tmp_path):
    """Test descending order and the top ten limit."""
    path = tmp_path / "highscore.json"
    highscore = Highscore(str(path))

    for i in range(12):
        highscore.add_score(f"PLAYER{i}", i * 100)

    scores = highscore.top_score()

    assert len(scores) == 10
    assert scores[0]["score"] == 1100
    assert scores[-1]["score"] == 200


def test_load_missing_file(tmp_path):
    """Test creating an empty file when none exists."""
    path = tmp_path / "highscore.json"
    highscore = Highscore(str(path))

    highscore.load_score()

    assert highscore.scores == []
    assert path.exists()
    assert json.loads(path.read_text()) == []


def test_load_corrupted_file(tmp_path):
    """Test handling invalid JSON without crashing."""
    path = tmp_path / "highscore.json"
    path.write_text("{invalid JSON")

    highscore = Highscore(str(path))
    highscore.load_score()

    assert highscore.scores == []


def test_load_saved_scores(tmp_path):
    """Test loading and sorting saved scores."""
    path = tmp_path / "highscore.json"
    path.write_text(
        json.dumps([
            {"name": "EMILIE", "score": 100},
            {"name": "PLAYER", "score": 500},
        ])
    )

    highscore = Highscore(str(path))
    highscore.load_score()

    assert highscore.scores == [
        {"name": "PLAYER", "score": 500},
        {"name": "EMILIE", "score": 100},
    ]


def test_add_score_save_failure(tmp_path, monkeypatch):
    """Restore scores when saving fails."""
    filepath = tmp_path / "highscores.json"
    filepath.write_text(
        '[{"name": "Alice", "score": 100}]',
        encoding="utf-8",
    )

    highscore = Highscore(str(filepath))
    highscore.load_score()
    original_scores = highscore.scores.copy()
    original_content = filepath.read_text(encoding="utf-8")

    def fail_save():
        return False

    monkeypatch.setattr(highscore, "save_score", fail_save)

    result = highscore.add_score("Bob", 200)

    assert result is False
    assert highscore.scores == original_scores
    assert filepath.read_text(encoding="utf-8") == original_content


def test_equal_scores_are_preserved(tmp_path):
    """Keep players with equal scores in the leaderboard."""
    filepath = tmp_path / "highscores.json"
    highscore = Highscore(str(filepath))
    highscore.load_score()

    assert highscore.add_score("Alice", 100)
    assert highscore.add_score("Bob", 100)

    scores = highscore.top_score()

    assert len(scores) == 2
    assert all(entry["score"] == 100 for entry in scores)
    assert {entry["name"] for entry in scores} == {"Alice", "Bob"}


def test_scores_persist_after_reload(tmp_path):
    """Keep saved scores available after reloading."""
    filepath = tmp_path / "highscores.json"

    highscore = Highscore(str(filepath))
    highscore.load_score()
    assert highscore.add_score("Alice", 100)
    assert highscore.add_score("Bob", 250)

    reloaded = Highscore(str(filepath))
    reloaded.load_score()

    assert reloaded.top_score() == [
        {"name": "Bob", "score": 250},
        {"name": "Alice", "score": 100},
    ]
