"""
An Enum class for holding the 8 types of commands.
"""

from enum import Enum

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

indirect = lambda x: [f"@{x}", "D=A", "@seg", "D=D+M", "@R13", "M=D"]

segment_map: dict = {
    "constant": lambda x: [f"@{x}", "D=A"],
    "local": indirect,
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

segment_memory_map: dict = {
    "local": "LCL",
}