import pytest

from src.data_storage import CommandType
import src.data_storage as data_storage
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
    translated_push_value: list[str] = translator.write_push_pop(CommandType.PUSH, "constant", 7)
    assert translated_push_value == ["@7", "D=A", "@SP", "AM=M+1", "A=A-1", "M=D"]


def test_write_arithmetic_add(setup_resources):
    """
    Test that we can output the add command
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["add"]
    translated_add_value: list[str] = translator.write_arithmetic("add")
    print(translated_add_value)
    assert translated_add_value == ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"]


def test_create_label(setup_resources):
    """
    Test that automatic labels are created.
    """
    translator = setup_resources["translator"]
    translated_line: list[str] = ["D=M-D", "M=-1", f"@LABEL", "JMP", "@SP", "A=M-1", "M=0", "(LABEL)"]
    new_line: list[str] = translator.generate_label("eq", translated_line)
    assert new_line == ["D=M-D", "M=-1", f"@eq.0", "JMP", "@SP", "A=M-1", "M=0", "(eq.0)"]

