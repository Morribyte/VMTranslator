"""
src/parser.py
Handles parsing the file and pulling out the lexical elements we need.
"""
from src.data_storage import CommandType, ARITHMETIC_COMMANDS


class Parser:
    """
    Represents a parser object
    """
    def __init__(self):
        self.command_line: list[str] = []

    def get_line(self, vm_command: str) -> list[str]:
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
        if self.command_line[0] in ARITHMETIC_COMMANDS:
            return CommandType.ARITHMETIC
        if "if-goto" in self.command_line[0]:
            return CommandType.IF
        return CommandType.__members__.get(self.command_line[0].upper(), None)

    def arg1(self) -> str | None:
        """
        Returns the segment if we need it.
        If the command type is either C_RETURN or C_ARITHMETIC, we will handle differently.
        """
        print(self.command_type())
        if self.command_type() == CommandType.ARITHMETIC:
            return self.command_line[0]
        return self.command_line[1]

    def arg2(self) -> int | None:
        """
        Returns the index if we need it.
        Called if the command_type is either C_PUSH, C_POP, C_FUNCTION, or C_CALL
        Not called if others.
        """
        return int(self.command_line[2])
