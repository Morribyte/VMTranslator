"""
src/parser_test.py
Handles parsing the file and pulling out the lexical elements we need.
"""
from src.command_type import CommandType


class Parser:
    """
    Represents a parser object
    """
    def __init__(self):
        self.command_line: list[str] = []
        self.command_type: CommandType

    def get_next_line(self, vm_command: str) -> list[str]:
        """
        Takes a string and splits it into a list.
        """
        self.command_line = vm_command.split()
        return self.command_line

    def command_type(self) -> CommandType | None:
        """
        Returns the command type of the current command.
        Command types will be one of 8 named in the CommandType enum class.
        """
        return CommandType.__members__.get(self.command_line[0].upper(), None)

