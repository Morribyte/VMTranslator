"""
src/translator.py
Converts VM code instructions to machine / assembly code.
"""
from typing import Optional

from src import data_storage as data_storage
from src.data_storage import CommandType, command_map, arithmetic_map, comparison_map, label_map, \
    segment_memory_map, pop_segment_map, push_segment_map, STATIC_VARIABLE_NUMBER
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
        if command == CommandType.POP:
            match segment:
                case "temp" | "pointer" | "static":
                    return command_map[command] + pop_segment_map[segment](index)
                case _:
                    return pop_segment_map[segment](index) + command_map[command] + pop_segment_map["end"]
        return push_segment_map[segment](index) + command_map[command]

    def write_arithmetic(self, command: str) -> list[str]:
        """
        Takes a command and translates it to a different command depending on what we need.
        """
        if command in comparison_map:  # Redirect to logical
           return command_map[CommandType.POP] + arithmetic_map["logical"]
        return arithmetic_map[command]

    def generate_label(self, command: str, translated_line: list[str]) -> list[str]:
        """
        Takes a list of commands and generates a label.
        Only applies to lt, gt, and eq commands.
        Command: lt, gt, or eq as a string
        Label_map[command]: we track the label we're using lt, gt, or eq using a dict and increment the proper command at the end
        """
        new_line: list[str] = [word.replace("LABEL", f"{command}.{label_map[command]}") for word in translated_line]
        label_map[command] += 1
        return new_line

    def write_jump(self, command: str, translated_line: list[str]) -> list[str]:
        """
        Replaces the jump directive with the proper jump command.
        """
        new_line: list[str] = [word.replace("JMP", f"D;J{command.upper()}") for word in translated_line]
        print(new_line)
        return new_line

    def write_segment(self, command: str, translated_line: list[str],  direct_memory_index: Optional[int] = None) -> list[str]:
        """
        Replaces a segment with the correct label
        """
        print(f"Command: {command}, {direct_memory_index}")
        new_line: list[str] = [word.replace("seg", f"{segment_memory_map[command](direct_memory_index)}") for word in translated_line]
        return new_line

    def set_arg2(self, arg2_value: int):
        data_storage.STATIC_VARIABLE_NUMBER = arg2_value

    def get_arg2(self) -> int:
        """
        Gets the current arg2 value from STATIC_VARIABLE_NUMBER.
        """
        return data_storage.STATIC_VARIABLE_NUMBER if data_storage.STATIC_VARIABLE_NUMBER is not None else None
