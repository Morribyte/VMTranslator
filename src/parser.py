"""
src/parser_test.py
Handles parsing the file and pulling out the lexical elements we need.
"""


class Parser:
    """
    Represents a parser object
    """
    def __init__(self):
        self.command_line: list[str] = []

    def get_next_line(self, vm_command: str) -> list[str]:
        """
        Takes a string and splits it into a list.
        """
        command: list[str] = vm_command.split()
        return command