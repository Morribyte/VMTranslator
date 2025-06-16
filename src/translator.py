"""
src/translator.py
Converts VM code instructions to machine / assembly code.
"""
from src.data_storage import CommandType

command_map: dict = {
    "push": ["@SP", "AM=M+1", "A=A-1", "M=D"]
}

class Translator:
    """
    Represents a translator object
    """
    def __init__(self):
        pass

    def write_push_pop(self, command: str):
        """
        Takes a command and depending on whether it's C_PUSH or C_POP, operate on it.
        """
