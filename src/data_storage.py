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

ARITHMETIC_COMMANDS = ["add"]
