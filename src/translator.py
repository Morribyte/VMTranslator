"""
src/translator.py
Converts VM code instructions to machine / assembly code.
"""
from src.data_storage import CommandType
from src.parser import Parser

command_map: dict = {
    CommandType.PUSH: ["@SP", "AM=M+1", "A=A-1", "M=D"]
}

segment_map: dict = {
    "constant": lambda x: [f"@{x}", "D=A"]
}

arithmetic_map: dict = {
    "logical": ["D=M-D", "M=-1", f"@LABEL", "JMP", "@SP", "A=M-1", "M=0", "(LABEL)"],
    "add": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"],
}

# op_type: dict = {
#     "binary_op": ["@SP", "AM=M-1", "D=M", "A=A-1"]
# }

class Translator:
    """
    Represents a translator object
    """
    def __init__(self):
        self.parser = Parser()

    def write_push_pop(self, command: CommandType, segment: str, index: int) -> list[str]:
        """
        Takes a command and depending on whether it's C_PUSH or C_POP, operate on it.
        """
        return segment_map[segment](index) + command_map[command]

    def write_arithmetic(self, command: str) -> list[str]:
        """
        Takes a command and translates it to a different command depending on what we need.
        """
        return arithmetic_map[command]

    def generate_label(self, command: str, label_number: int, translated_line: list[str]) -> list[str]:
        """
        Takes a list of commands and generates a label.
        Only applies to lt, gt, and eq commands.
        Command: lt, gt, or eq as a string
        Label_number: the number given at the start of the command in the loop, increments for each line.
        """

        appended_labels: list[str] = translated_line
        return appended_labels
