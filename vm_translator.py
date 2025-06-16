"""
root/vm_translator
Handles the orchestration of the VM translation process.
"""
import argparse
from pathlib import Path

def get_file():
    """
    Prompts user for a file if not provided via command-line.
    """
    while True:
        file_path = input("Hack assembler > ").strip()
        if Path(file_path).exists():
            return file_path
        print("File not found. Try again.")


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


if __name__ == "__main__":
    main()