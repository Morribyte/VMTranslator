import pytest

from src.data_storage import CommandType
import src.data_storage as data_storage
from src.translator import Translator

@pytest.fixture(scope="module")
def setup_resources():
    """
    Sets up the translator object for testing.
    """
    translator = Translator()

    yield {
        "translator": translator,
    }


def test_object_creation(setup_resources):
    """
    Test that translator object is created properly
    """
    translator = setup_resources["translator"]
    assert translator is not None


def test_write_push_pop(setup_resources):
    """
    Test that the push function properly translates.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["push", "constant", "7"]
    translated_push_value: list[str] = translator.write_push_pop(CommandType.PUSH, "constant", 7)
    assert translated_push_value == ["@7", "D=A", "@SP", "AM=M+1", "A=A-1", "M=D"]


def test_write_arithmetic_add(setup_resources):
    """
    Test that we can output the add command
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["add"]
    translated_add_value: list[str] = translator.write_arithmetic("add")
    print(translated_add_value)
    assert translated_add_value == ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M"]


def test_create_label(setup_resources):
    """
    Test that automatic labels are created.
    """
    translator = setup_resources["translator"]
    translated_line: list[str] = ["D=M-D", "M=-1", f"@LABEL", "JMP", "@SP", "A=M-1", "M=0", "(LABEL)"]
    print(translated_line)
    new_line: list[str] = translator.generate_label("eq",  translated_line)
    print(new_line)
    assert new_line == ["D=M-D", "M=-1", f"@eq.0", "JMP", "@SP", "A=M-1", "M=0", "(eq.0)"]
    data_storage.label_map = {
        "eq": 0,
        "lt": 0,
        "gt": 0,
    }

@pytest.mark.parametrize("loop_list", ["eq", "gt", "lt"])
def test_looped_label_eq(setup_resources, loop_list):
    """
    Test that our loop label starts back at 0 when moving on and increments in a loop properly.
    """
    translator = setup_resources["translator"]
    line_count = 0
    print(data_storage.label_map)

    for loop_items in range(10):
        print(data_storage.label_map)
        translated_line: list[str] = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=M-D', 'M=-1', f'@{loop_list}.{line_count}', 'JMP', '@SP',
                                      'A=M-1', 'M=0', f'({loop_list}.{line_count})']

        new_line: list[str] = translator.generate_label(loop_list, translated_line)
        print(new_line)
        assert new_line == translated_line
        line_count += 1


def test_arithmetic_command_returns_logical(setup_resources):
    """
    Test that when an arithmetic command is returned, the method outputs logical
    """
    translator = setup_resources["translator"]
    line = translator.write_arithmetic("eq")
    assert line == [ "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1", f"@LABEL", "JMP", "@SP", "A=M-1", "M=0", "(LABEL)"]


def test_arithmetic_comparison_replace_jump(setup_resources):
    """
    Test that when an arithmetic command is comparison, we replace the JMP directive with the proper label.
    """
    translator = setup_resources["translator"]
    translated_line: list[str] = ['@SP', 'AM=M-1', 'D=M', 'A=A-1', 'D=M-D', 'M=-1', f'@', 'JMP',
                                  '@SP',
                                  'A=M-1', 'M=0', f'()']
    line = translator.write_jump("eq", translated_line)
    assert line[7] == "D;JEQ"


def test_pop_local_segment(setup_resources):
    """
    Test that when we use pop and local, we correctly translate into the code we need
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["pop", "local", "0"]
    translated_pop_value: list[str] = translator.write_push_pop(CommandType.POP, "local", 0)
    assert translated_pop_value == ['@0', 'D=A', '@seg', 'D=D+M', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']


def test_local_segment_replacement(setup_resources):
    """
    Test that the @seg gets replaced with LCL properly.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["pop", "local", "0"]
    translated_line: list[str] = translator.write_push_pop(CommandType.POP, "local", 0)
    print(f"translated_line: {translated_line}")
    assert translated_line == ['@0', 'D=A', '@seg', 'D=D+M', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D']
    line = translator.write_segment("local", translated_line)
    print(f"after line: {line}")
    assert "@LCL" in line[2]


def test_temp_replaces_seg(setup_resources):
    """
    Test that we can use the new dict for mapping the direct memory access pointers to the correct address
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["push", "temp", "0"]
    line: list[str] = [f"@seg", "D=M", "@SP", "AM=M+1", "A=A-1", "M=D"]
    line = translator.write_segment("temp", line, direct_memory_index=0)
    print(f"translated_line: {line}")
    assert line == [f"@5", "D=M", "@SP", "AM=M+1", "A=A-1", "M=D"]


def test_set_arg2_for_static(setup_resources):
    """
    Test that when we use set_arg2 for static, it returns the proper value.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["push", "temp", "3"]
    arg_2 = translator.set_arg2(3)
    assert data_storage.STATIC_VARIABLE_NUMBER == 3


def test_get_arg2_for_static(setup_resources):
    """
    Test that when we use get_arg2 for static variables, it returns proper value.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["push", "temp", "3"]
    translator.set_arg2(3)
    assert translator.get_arg2() == 3


def test_default_case_push_pop(setup_resources):
    """
    Test that we execute the default case in our push_pop method
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["pop", "temp", "7"]
    translated_pop_value: list[str] = translator.write_push_pop(CommandType.POP, "temp", 7)
    assert translated_pop_value == ['@SP', 'AM=M-1', 'D=M', '@seg', 'M=D']


def test_label_command(setup_resources):
    """
    Test that when we execute the label command, it properly writes teh label we need.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["label", "LOOP"]
    data_storage.FUNCTION_NAME = "Main.main"
    translated_label: list[str] = translator.write_label("LOOP")
    print(translated_label)
    assert translated_label == ["(Main.main$LOOP)"]


def test_if_goto_command(setup_resources):
    """
    Test that when we execute the IF command, it properly writes the label we need.
    """
    translator = setup_resources["translator"]
    data_storage.FUNCTION_NAME = "Main.main"
    translator.parser.command_line = ["if-goto", "LOOP"]
    translated_label: list[str] = translator.write_if_goto("LOOP")
    print(translated_label)
    assert translated_label == ['@SP', 'AM=M-1', 'D=M', '@Main.main$LOOP', 'D;JNE']


def test_goto_command(setup_resources):
    """
    Test that when we execute the goto command, it properly writes the label we need.
    """
    translator = setup_resources["translator"]
    data_storage.FUNCTION_NAME = "Main.main"
    translator.parser.command_line = ["goto", "LOOP"]
    translated_label: list[str] = translator.write_goto("LOOP")
    print(translated_label)
    assert translated_label == ["@Main.main$LOOP", "0;JMP"]


def test_function_command(setup_resources):
    """
    Test that when we execute the function command, it properly creates the assembly we need.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["function", "SimpleFunction.test", "2"]
    translated_function: list[str] = translator.write_compact_function("SimpleFunction.test", 2)
    print(translated_function)
    assert translated_function ==  ["(SimpleFunction.test)", "@0", "D=A", "@SP", "AM=M+1", "A=A-1", "M=D"] or translated_function == ['(SimpleFunction.test)', '@2', 'D=A', '(init_lcl.0)', '@SP', 'AM=M+1', 'A=A-1', 'M=0', 'D=D-1', '@init_lcl.0', 'D;JGT']


def test_return_command(setup_resources):
    """
    Test that when we execute the return command, it properly translates the assembly we need.
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["return"]
    translated_return: list[str] = translator.write_return()
    print(translated_return)
    assert translated_return == ["@LCL", "D=M", "@R13", "M=D",  # get address at frame end
                         "@5", "A=D-A", "D=M",  # calculate return address
                         "@R14", "M=D", "@SP", "A=M-1", "D=M",  # Place return value for caller
                         "@ARG", "A=M", "M=D", "@ARG", "D=M", "@SP", "M=D+1",
                         '@R13', 'M=M-1', 'A=M', 'D=M', '@THAT', 'M=D',
                         '@R13', 'M=M-1', 'A=M', 'D=M', '@THIS', 'M=D',
                         '@R13', 'M=M-1', 'A=M', 'D=M', '@ARG', 'M=D',
                         '@R13', 'M=M-1', 'A=M', 'D=M', '@LCL', 'M=D',
                         "@R14", "A=M", "0;JMP"] or translated_return == ['@2', 'D=A', '(init_lcl.0)', '@SP', 'AM=M+1', 'A=A-1', 'M=0', 'D=D-1', '@init_lcl.0', 'D;JGT']


def test_call_save_frame(setup_resources):
    """
    Test the save frame method
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["call", "Main.main", 2]
    the_list = translator.write_save_frame()
    print(the_list)
    assert the_list == ['@LCL', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@ARG', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@THIS', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@THAT', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D']


def test_call_command_push_return_address(setup_resources):
    """
    Test that when we do the call command, we push the return address
    """
    translator = setup_resources["translator"]
    translator.parser.command_line = ["call", "Main.main", 2]
    the_list = translator.write_call("Main.main", 2)
    print(the_list)
    assert the_list == ["@2", "D=A", "@R13", "M=D",
                        "@Main.main$ret.0", "D=A", "@SP", "AM=M+1", "A=A-1", "M=D",
                        '@LCL', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@ARG', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@THIS', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@THAT', 'D=M', '@SP', 'AM=M+1', 'A=A-1', 'M=D',
                        '@R13', 'D=M', '@5', 'D=D+A', '@SP', 'D=M-D', '@ARG', 'M=D',
                        '@SP', 'D=M', '@LCL', 'M=D',
                        '@Main.main', '0;JMP', '(Main.main$ret.0)']


def test_bootstrap_code(setup_resources):
    """
    Test that when we call the bootstrap_init() method, the correct bootstrap code is emitted.
    """
    translator = setup_resources["translator"]
    bootstrap = translator.write_bootstrap()
    print(bootstrap)
    assert bootstrap == ["@256", "D=A", "@SP", "M=D", "call Sys.init 0"]