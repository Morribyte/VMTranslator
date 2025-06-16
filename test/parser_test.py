import pytest

from src.parser import Parser

@pytest.fixture
def setup_resources():
    """
    Sets up the parser object for testing.
    """
    parser = Parser()

    yield {
        "parser": parser,
    }


def test_object_creation(setup_resources):
    """
    Test that parser object is created properly
    """
    parser = setup_resources["parser"]
    assert parser is not None


def test_get_line(setup_resources):
    """
    Test that the parser can read commands and parse them.
    """
    parser = setup_resources["parser"]
    value = parser.command_type("push constant 7")
    assert value == ["push", "constant", "7"]

