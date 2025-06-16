"""
root/vm_translator
Handles the orchestration of the VM translation process.
"""
import argparse
from pathlib import Path

from src.data_storage import CommandType
from src.parser import Parser
from src.translator import Translator

parser = Parser()
translator = Translator()

def get_file():
    """
    Prompts user for a file if not provided via command-line.
    """
    while True:
        file_path = input("Hack assembler > ").strip()
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
    if current_command in [CommandType.PUSH]:
        arg2: int = parser.arg2()
    else:
        arg2: None = None
    return current_command, arg1, arg2


def write_to_file(file_name: str, code_file: list[str]):
    """
    Writes a translated list to a file, line by line.
    """
    with open(f"output/{file_name}.asm", "w") as file:
        print(f"Translated VM File @ output/{file_name}.hack")
        file.writelines(f"// Translated VM File @ output/{file_name}.hack\n")

        for index, line in enumerate(code_file):
            translated_line = []
            print(f"\nIndex: {index} | Line: {line}")

            split_line: list[str] = parser.get_line(line)
            print(f"{split_line}")

            current_command, arg1, arg2 = process_command_arguments()

            print(f"Current command: {current_command} | Current arg1: {arg1} | Current arg2: {arg2}")
            file.writelines(f"// {line}\n")


            match current_command:
                case CommandType.PUSH | CommandType.POP:
                    translated_line = translator.write_push_pop(current_command, arg1, arg2)
                case CommandType.ARITHMETIC:
                    translated_line = translator.write_arithmetic(arg1)


            print(f"Translated line: {translated_line}")
            file.writelines(f"{line}\n" for line in translated_line)





def main():
    """
    main function
    """
    parse = argparse.ArgumentParser(description="HACK Assembler")
    parse.add_argument("file", nargs="?", help="Assembles the given file into a .hack file.")

    args = parse.parse_args()
    file_path: Path = Path(args.file if args.file else get_file())
    file_name: str = file_path.stem

    print(f"Current file path: {file_path}")
    print(f"Current file name: {file_path.stem}")

    open_file = read_file(file_path)

    print(f"Translating file...\n")

    write_to_file(file_name, open_file)


if __name__ == "__main__":
    main()
