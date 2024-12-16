import sys
from vm_translator import VMTranslator


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    input_path = sys.argv[1]
    translator = VMTranslator(input_path)
    translator.translate()


if __name__ == "__main__":
    main()