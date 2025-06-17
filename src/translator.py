"""
src/translator.py
Converts VM code instructions to machine / assembly code.
"""
from src.data_storage import CommandType, command_map, segment_map, arithmetic_map, comparison_map, label_map
from src.parser import Parser


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
        if command in comparison_map:  # Redirect to logical
           return arithmetic_map["logical"]
        return arithmetic_map[command]

    def generate_label(self, command: str, translated_line: list[str]) -> list[str]:
        """
        Takes a list of commands and generates a label.
        Only applies to lt, gt, and eq commands.
        Command: lt, gt, or eq as a string
        Label_number: the number given at the start of the command in the loop, increments for each line.
        """
        new_line: list[str] = [word.replace("LABEL", f"{command}.{label_map[command]}") for word in translated_line]
        label_map[command] += 1
        return new_line
