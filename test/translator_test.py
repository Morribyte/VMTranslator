import pytest

from src.data_storage import CommandType
from src.translator import Translator

@pytest.fixture(scope="module")
def setup_resources():
    """
    Sets up the translator object for testing.
    """
    translator = Translator()

    yield {
        "translator": translator,
    }


def test_object_creation(setup_resources):
    """
    Test that translator object is created properly
    """
    translator = setup_resources["translator"]
    assert translator is not None


def test_write_push_pop(setup_resources):
    """
    Test that the push function properly translates.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["push", "constant", "7"]
    translated_push_value: list[str] = translator.write_push_pop("push", "constant", 7)
    assert translated_push_value == ["@7", "D=A", "@SP", "AM=M+1", "A=A-1", "M=D"]
