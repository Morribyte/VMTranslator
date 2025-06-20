"""
An Enum class for holding the 8 types of commands.
"""

from enum import Enum
from typing import Callable

# To simplify the write_segment method, I decided it'd be best to create a helper function so that the dict stores
# only callables. For the segments that don't require direct address replacements, I can use the function as a callable
# replacement to make sure the code doesn't produce errors.

class CommandType(Enum):
    ARITHMETIC = "C_ARITHMETIC"
    PUSH = "C_PUSH"
    POP = "C_POP"
    LABEL = "C_LABEL"
    GOTO = "C_GOTO"
    IF = "C_IF"
    FUNCTION = "C_FUNCTION"
    RETURN = "C_RETURN"
    CALL = "C_CALL"

ARITHMETIC_COMMANDS = ["add", "sub", "neg", "and", "not", "or", "eq", "lt", "gt"]

command_map: dict = {
    CommandType.PUSH: ["@SP", "AM=M+1", "A=A-1", "M=D"],
    CommandType.POP: ["@SP", "AM=M-1", "D=M"]
}

push_indirect_segment = lambda x: [f"@{x}", "D=A", "@seg", "A=D+M", "D=M", "@R13"]
push_direct_segment = lambda x: [f"@seg", "D=M"]

push_segment_map: dict = {
    "constant": lambda x: [f"@{x}", "D=A"],
    "local": push_indirect_segment,
    "argument": push_indirect_segment,
    "this": push_indirect_segment,
    "that": push_indirect_segment,
    "temp": push_direct_segment,
}

pop_indirect_segment = lambda x: [f"@{x}", "D=A", "@seg", "D=D+M", "@R13", "M=D"]
pop_direct_segment = lambda x: ["@seg", "M=D"]

pop_segment_map: dict = {
    "constant": lambda x: [f"@{x}", "D=A"],
    "local": pop_indirect_segment,
    "argument": pop_indirect_segment,
    "this": pop_indirect_segment,
    "that": pop_indirect_segment,
    "temp": pop_direct_segment,
    "pointer": pop_direct_segment,
    "end": ["@R13", "A=M", "M=D"]
}
arithmetic_map: dict = {
    "logical": ["A=A-1", "D=M-D", "M=-1", f"@LABEL", "JMP", "@SP", "A=M-1", "M=0", "(LABEL)"],  # eq, gt, lt
    "add": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"],
    "sub": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D"],
    "neg": ["@SP", "A=M-1", "M=-M"],
    "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M"],
    "or": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D|M"],
    "not": ["@SP", "A=M-1", "M=!M"]
}

comparison_map: list = ["lt", "gt", "eq"]

label_map: dict = {
    "eq": 0,
    "lt": 0,
    "gt": 0,
}

segment_memory_map: dict[str, Callable[[int], str]] = {
    "local": lambda _: "LCL",
    "argument": lambda _: "ARG",
    "this": lambda _: "THIS",
    "that": lambda _: "THAT",
    "temp": lambda x: f"{5 + x}",
    "pointer": lambda x: "THIS" if x==0 else "THAT",
}
