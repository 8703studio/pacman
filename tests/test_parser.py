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

    config = parser.build_config(str(p))
    assert isinstance(config, dict)
    assert config["lives"] == 5
    assert config["seed"] == 123
    assert config["pacgum"] == 42


def test_file_not_found(parser):
    config = parser.build_config("inexistant.json")
    assert isinstance(config, dict)
    assert config["lives"] == 3
    assert config["seed"] == 42


def test_invalid_json_syntax(parser, tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{ mauvais json : sans guillemets }")

    config = parser.build_config(str(p))
    assert isinstance(config, dict)
    assert config["lives"] == 3


def test_invalid_values_fallback(parser, tmp_path):
    config_data = {
        "lives": -2,
        "pacgum": "pas_un_nombre"
    }
    p = tmp_path / "invalid_vals.json"
    p.write_text(json.dumps(config_data))

    config = parser.build_config(str(p))
    assert isinstance(config, dict)
    assert config["lives"] == 3
    assert config["pacgum"] == 42
