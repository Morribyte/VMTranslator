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


def read_file(file_path):
    """
    Opens a file, and strips comments whether they're at the start or at the end of a line.
    """
    with open(file_path, "r") as file:
        lines: list[str] = [line.split("//")[0].rstrip() for line in file.readlines() if line.split("//")[0].strip()]
    lines = [line.strip() for line in lines]
    print(lines)
    return lines


def process_command_arguments():
    current_command: CommandType = parser.command_type()
    if current_command != CommandType.RETURN:
        arg1: str = parser.arg1()
    else:
        arg1: None = None
    if current_command in [CommandType.PUSH, CommandType.POP]:
        arg2: int = parser.arg2()
    else:
        arg2: None = None
    return current_command, arg1, arg2


def write_to_file(file_name: str, code_file: list[str]):
    """
    Writes a translated list to a file, line by line.
    """
    label_count: int = 0
    with open(f"output/{file_name}.asm", "w") as file:
        print(f"Translated VM File @ output/{file_name}.asm")
        file.writelines(f"// Translated VM File @ output/{file_name}.asm\n")
        translated_line: list[str] = []

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
            print(f"Translated line: {translated_line}")
            file.writelines(f"{line}\n" for line in translated_line)

def main():
    """
    main function
    """
    parse = argparse.ArgumentParser(description="HACK Assembler")
    parse.add_argument("file", nargs="?", help="Assembles the given file into a .hack file.")

    args = parse.parse_args()
    data_storage.FILE_PATH = Path(args.file if args.file else get_file())
    data_storage.FILE_NAME = data_storage.FILE_PATH.stem

    print(f"Current file path: {data_storage.FILE_PATH}")
    print(f"Current file name: {data_storage.FILE_NAME}")

    open_file = read_file(data_storage.FILE_PATH)

    print(f"Translating file...\n")

    write_to_file(data_storage.FILE_NAME, open_file)


if __name__ == "__main__":
    main()
