import json

import pytest

from src.config.parser import Parser


@pytest.fixture
def parser():
    return Parser()


def test_load_valid_config(parser, tmp_path):
    p = tmp_path / "config.json"
    p.write_text("""
    # this is a comment test
    {
        "lives": 5,
        "seed": 123
    }
    """)

    data = parser.build_config(str(p))

    assert isinstance(data, dict)
    assert data["lives"] == 5
    assert data["seed"] == 123


def test_file_not_found(parser):
    data = parser.build_config("inexistant.json")

    assert data == {}


def test_invalid_json_syntax(parser, tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{ bad json 2 }")

    data = parser.build_config(str(p))

    assert data == {}


def test_invalid_values(parser, tmp_path):
    config_data = {
        "lives": -2,
        "pacgum": "not a number"
    }

    p = tmp_path / "invalid_vals.json"
    p.write_text(json.dumps(config_data))

    data = parser.build_config(str(p))

    assert data["lives"] == -2
    assert data["pacgum"] == "not a number"
