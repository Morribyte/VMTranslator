import pytest

from src.command_type import CommandType
from src.parser import Parser

@pytest.fixture(scope="module")
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
    value: CommandType = parser.command_type()
    print(value.value)
    assert value.value == "C_PUSH"


def test_arg1_returns_string(setup_resources):
    """
    Test that our arg1 properly returns the string it needs to.
    """
    parser = setup_resources["parser"]
    command_list: list[str] = ["push", "constant", "7"]
    value: str = parser.arg1()
    assert value == "constant"


def test_arg1_c_return_returns_none(setup_resources):
    """
    Test that arg1 returns None in the case of C_RETURN.
    """
    parser = setup_resources["parser"]
    parser.get_next_line("return")
    value: CommandType = parser.command_type()
    value: str = parser.arg1()
    assert value is None


def test_arg1_c_arithmetic_returns_command(setup_resources):
    """
    Test that arg1 returns the first portion of the list in case of C_ARITHMETIC
    """
    parser = setup_resources["parser"]
    parser.get_next_line("add")
    value: CommandType = parser.command_type()
    value: str = parser.arg1()
    assert value == "add"
