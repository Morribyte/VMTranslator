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
    value = parser.get_next_line("push constant 7")
    assert value == ["push", "constant", "7"]


def test_command_type(setup_resources):
    """
    Test that we can grab the first argument of any command and have it be returned.
    """
    parser = setup_resources["parser"]
    command_list: list[str] = ["push", "constant", "7"]
    value: str = parser.command_type()
    assert value == "C_PUSH"
