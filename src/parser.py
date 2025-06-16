"""
src/parser_test.py
Handles parsing the file and pulling out the lexical elements we need.
"""


class Parser:
    """
    Represents a parser object
    """
    def __init__(self):
        pass

    def command_type(self, vm_command: str) -> list[str]:
        """
        Takes a string and splits it into a list.
        """
        return "push constant 7"