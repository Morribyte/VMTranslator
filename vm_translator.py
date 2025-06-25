"""
root/vm_translator
Handles the orchestration of the VM translation process.
"""
import argparse
from pathlib import Path

from src.data_storage import CommandType
import src.data_storage as data_storage
from src.parser import Parser
from src.translator import Translator

parser = Parser()
translator = Translator()

def get_file():
    """
    Prompts user for a file if not provided via command-line.
    """
    while True:
        file_path = input("Hack VMTranslator > ").strip()
        if Path(file_path).exists():
            return file_path
        print("File not found. Try again.")


def read_file(file_paths):
    """
    Opens a file, and strips comments whether they're at the start or at the end of a line.
    """
    all_lines: dict[str, str] = {}
    for file_path in file_paths:
        print(f"Reading: {file_path}")
        file_name = Path(file_path).stem
        with open(file_path, "r") as file:
            lines: list[str] = [line.split("//")[0].rstrip() for line in file.readlines() if line.split("//")[0].strip()]
        all_lines[file_name] = lines
    print(all_lines)
    return all_lines


def process_command_arguments():
    current_command: CommandType = parser.command_type()
    if current_command != CommandType.RETURN:
        arg1: str = parser.arg1()
    else:
        arg1: None = None
    if current_command in [CommandType.PUSH, CommandType.POP, CommandType.FUNCTION, CommandType.CALL]:
        arg2: int = parser.arg2()
    else:
        arg2: None = None
    return current_command, arg1, arg2


def write_to_file(file_name: str, code_to_translate: dict[str, str]):
    """
    Writes a translated list to a file, line by line.
    """
    label_count: int = 0
    with open(f"output/{file_name}.asm", "w") as file:
        print(f"Translated VM File @ output/{file_name}.asm")
        file.writelines(f"// Translated VM File @ output/{file_name}.asm\n")
        translated_line: list[str] = []

        # Bootstrap code, written manually.
        file.writelines(f"{line}\n" for line in data_storage.system_initialization)
        file.writelines("\n".join(translator.write_call("Sys.init", 0)) + "\n")

        for file_name, code_file in code_to_translate.items():
            data_storage.FILE_NAME = file_name

            for index, line in enumerate(code_file):

                print(f"\nIndex: {index} | Line: {line}")

                split_line: list[str] = parser.get_line(line)
                print(f"{split_line}")

                current_command, arg1, arg2 = process_command_arguments()

                print(f"Current command: {current_command} | Current arg1: {arg1} | Current arg2: {arg2}")
                file.writelines(f"// {line}\n")

                match current_command:
                    case CommandType.PUSH | CommandType.POP:
                        translator.set_arg2(arg2)
                        translated_line = translator.write_push_pop(current_command, arg1, arg2)
                        if arg1 != "constant":
                            translated_line = translator.write_segment(arg1, translated_line, arg2)
                    case CommandType.ARITHMETIC:
                        translated_line = translator.write_arithmetic(arg1)
                        print(f"CommandType is ARITHMETIC. Command: {arg1}")
                        if arg1 in data_storage.comparison_map:
                            print(f"Comparison label found: {current_command}")
                            translated_line = translator.generate_label(arg1, translated_line)
                            translated_line = translator.write_jump(arg1, translated_line)
                    case CommandType.FUNCTION:
                        print("Generating function")
                        print("Saving function name...")
                        data_storage.FUNCTION_NAME = arg1
                        translated_line = translator.write_function(arg1, arg2)
                    case CommandType.CALL:
                        print("Generating call")
                        translated_line = translator.write_call(arg1, arg2)
                    case CommandType.LABEL:
                        print("Generating Label")
                        translated_line = translator.write_label(arg1)
                    case CommandType.GOTO:
                        print(f"Generating Unconditional Goto")
                        translated_line = translator.write_goto(arg1)
                    case CommandType.IF:
                        print(f"Generating Conditional Goto")
                        translated_line = translator.write_if_goto(arg1)
                    case CommandType.RETURN:
                        print(f"Generating return")
                        print(f"Restoring Pointers")
                        translated_line = translator.write_return()
                print(f"Translated line: {translated_line}")
                file.writelines(f"{line}\n" for line in translated_line)

def main():
    """
    main function
    """
    parse = argparse.ArgumentParser(description="HACK VMTranslatorr")
    parse.add_argument("file", nargs="?", help="Translates the given file into a .hack file.")

    args = parse.parse_args()
    file_list: list[Path] = []
    data_storage.FILE_PATH = Path(args.file if args.file else get_file())
    data_storage.FILE_NAME = data_storage.FILE_PATH.stem
    data_storage.FILE_FOLDER = data_storage.FILE_PATH.parent

    print(f"Current file path: {data_storage.FILE_PATH}")
    print(f"Current file name: {data_storage.FILE_NAME}")
    print(f"Current folder: {data_storage.FILE_FOLDER}")

    if data_storage.FILE_PATH.is_dir():
        file_list = [file for file in data_storage.FILE_PATH.glob("*.vm")]
        print(f"Files to translate: {file_list}")
    elif data_storage.FILE_PATH.is_file():
        file_list = [data_storage.FILE_PATH]
        print(f"File to translate: {data_storage.FILE_PATH}")

    open_file = read_file(file_list)

    print(f"Translating file...\n")

    write_to_file(data_storage.FILE_NAME, open_file)


if __name__ == "__main__":
    main()
